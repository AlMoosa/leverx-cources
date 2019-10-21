import pymysql
import json
from dicttoxml import dicttoxml
import xml.dom.minidom
from xml.dom.minidom import parseString
import datetime
import decimal
from cli import parser


class FileReader():
    def __init__(self, path):
        self.path = path

    def read(self):
        raise NotImplementedError


class JsonReader(FileReader):
    def __init__(self, path):
        super().__init__(path)

    def read(self):
        try:
            with open(self.path, "r") as read_file:
                return json.load(read_file)

        except FileNotFoundError:
            return "File {} not found!".format(self.path)


class FileSaver():
    def __init__(self, result, filename):
        self.result = result
        self.filename = filename

    def save(self):
        raise NotImplementedError


class JsonSaver(FileSaver):
    def __init__(self, result, filename):
        super().__init__(result, filename)

    def myconverter(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.__str__()
        elif isinstance(obj, decimal.Decimal):
            return obj.__str__()

    def save(self):
        with open(self.filename, "w") as write_file:
            json.dump(self.result, write_file, sort_keys=True,
                      indent=4, default=self.myconverter)


class XmlSaver(FileSaver):
    def __init__(self, result, filename):
        super().__init__(result, filename)

    def save(self):
        xml = dicttoxml(self.result).decode('utf-8')
        dom = parseString(xml)
        with open(self.filename, "w") as xml_file:
            dom.writexml(xml_file, indent='\n', addindent='\t')


class DatabaseConnector:
    def __init__(self, host, user, password, db):
        self._conn = pymysql.connect(
            host,
            user,
            password,
            db,
            cursorclass=pymysql.cursors.DictCursor
        )
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()


def adding_data_to_db(students_path, rooms_path,
                      output_format, db_host,
                      db_user, db_password,
                      db_name):

    with DatabaseConnector(db_host, db_user, db_password, db_name) as db:
        rooms = JsonReader(rooms_path).read()
        for room in rooms:
            db.execute(
                'INSERT INTO Rooms (id,name) VALUES (%s,%s)',
                (room['id'], room['name'])
            )

    with DatabaseConnector(db_host, db_user, db_password, db_name) as db:
        students = JsonReader(students_path).read()
        for student in students:
            db.execute(
                'INSERT INTO Students (id,name,room,birthday,sex) VALUES (%s,%s,%s,%s,%s)',
                (student['id'], student['name'], student['room'],
                    student['birthday'], student['sex'])
            )


def executing_queries(db_host,
                      db_user, db_password,
                      db_name):
    result = []
    queries = [
        """SELECT Rooms.name AS ROOM_NAME, COUNT(room) AS NUM_OF_STUDENTS FROM
        Students INNER JOIN Rooms ON Rooms.id = Students.room GROUP BY room""",
        """SELECT Rooms.name AS ROOM, AVG((TO_DAYS(NOW())-TO_DAYS(birthday))/365)
        AS AVG_AGE FROM Students INNER JOIN Rooms ON Rooms.id = Students.room
        GROUP BY Rooms.name ORDER BY AVG_AGE LIMIT 5""",
        """SELECT Rooms.name AS ROOM,
        ((MAX((TO_DAYS(NOW())-TO_DAYS(birthday)))- MIN((TO_DAYS(NOW())-TO_DAYS(birthday))))/365)
        AS DIFF FROM Students INNER JOIN Rooms ON Rooms.id = Students.room GROUP
        BY Rooms.name ORDER BY DIFF DESC LIMIT 5""",
        """SELECT Rooms.name FROM Rooms INNER JOIN Students ON Students.room = Rooms.id
        GROUP BY Rooms.id HAVING COUNT(DISTINCT Students.sex)>=2""",
    ]

    with DatabaseConnector(db_host, db_user, db_password, db_name) as db:
        for query in queries:
            res_sql = db.query(query)
            result.append(res_sql)

    return result


def main(students_path, rooms_path,
         output_format, db_host,
         db_user, db_password,
         db_name):

    add_data_to_db(students_path, rooms_path,
                   output_format, db_host,
                   db_user, db_password,
                   db_name)

    result = queries_to_db(db_host,
                           db_user, db_password,
                           db_name)

    if output_format == 'json':
        for index, value in enumerate(result):
            JsonSaver(value, 'query{}.json'.format(index)).save()
    elif output_format == 'xml':
        for index, value in enumerate(result):
            XmlSaver(value, 'query{}.xml'.format(index)).save()
    else:
        print('Check output format')


if __name__ == "__main__":
    args = parser()

    students_path = args.path1
    rooms_path = args.path2
    output_format = args.format
    db_host = args.host
    db_user = args.user
    db_password = args.password
    db_name = args.db

    main(
        students_path,
        rooms_path,
        output_format,
        db_host,
        db_user,
        db_password,
        db_name
    )

# to run: python3 task4.py 'students.json' 'rooms.json' 'json' 'localhost' 'user' 'password' 'database_name'
