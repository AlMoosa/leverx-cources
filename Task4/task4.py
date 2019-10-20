import pymysql
import json
from dicttoxml import dicttoxml
import xml.dom.minidom
from xml.dom.minidom import parseString
import datetime
import decimal
from cli import parser


class ReadFile():
    def __init__(self, path):
        self.path = path

    def read(self):
        raise NotImplementedError


class ReadJson(ReadFile):
    def __init__(self, path):
        super().__init__(path)

    def read(self):
        try:
            with open(self.path, "r") as read_file:
                return json.load(read_file)

        except FileNotFoundError:
            return "File {} not found!".format(self.path)


class SaveFile():
    def __init__(self, result, filename):
        self.result = result
        self.filename = filename

    def save(self):
        raise NotImplementedError


class SaveToJson(SaveFile):
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


class SaveToXml(SaveFile):
    def __init__(self, result, filename):
        super().__init__(result, filename)

    def save(self):
        with open(self.filename, "w") as xml_file:
            self.result.writexml(xml_file, indent='\n', addindent='\t')


class Database:

    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def __connect__(self):
        self.con = pymysql.connect(host=self.host, user=self.user,
                                   password=self.password, db=self.db,
                                   cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.commit()
        self.con.close()

    def fetch(self, sql, params=None):
        self.__connect__()
        self.cur.execute(sql, params or ())
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def execute(self, sql, params=None):
        self.__connect__()
        self.cur.execute(sql, params or ())
        self.__disconnect__()


def add_data_to_db(students_path, rooms_path,
                   output_format, db_host,
                   db_user, db_password,
                   db_name):

    db = Database(db_host, db_user, db_password, db_name)
    rooms = ReadJson(rooms_path).read()
    for room in rooms:
        db.execute(
            'INSERT INTO Rooms (id,name) VALUES (%s,%s)',
            (room['id'], room['name'])
        )

    students = ReadJson(students_path).read()
    for student in students:
        db.execute(
            'INSERT INTO Students (id,name,room,birthday,sex) VALUES (%s,%s,%s,%s,%s)',
            (student['id'], student['name'], student['room'],
                student['birthday'], student['sex'])
        )


def queries_to_db(db_host,
                  db_user, db_password,
                  db_name):
    result = []
    queries = [
        "SELECT Rooms.name AS ROOM_NAME, COUNT(room) AS NUM_OF_STUDENTS FROM Students INNER JOIN Rooms ON Rooms.id = Students.room GROUP BY room",
        "SELECT Rooms.name AS ROOM, AVG((TO_DAYS(NOW())-TO_DAYS(birthday))/365) AS AVG_AGE FROM Students INNER JOIN Rooms ON Rooms.id = Students.room GROUP BY Rooms.name ORDER BY AVG_AGE LIMIT 5",
        "SELECT Rooms.name AS ROOM, ((MAX((TO_DAYS(NOW())-TO_DAYS(birthday)))- MIN((TO_DAYS(NOW())-TO_DAYS(birthday))))/365) AS DIFF FROM Students INNER JOIN Rooms ON Rooms.id = Students.room GROUP BY Rooms.name ORDER BY DIFF DESC LIMIT 5",
        "SELECT DISTINCT Rooms.name AS ROOM_NAME FROM Rooms INNER JOIN Students ON Students.room = Rooms.id WHERE sex = 'M' AND Rooms.name IN (SELECT Rooms.name AS ROOM_NAME FROM Rooms INNER JOIN Students ON Students.room = Rooms.id WHERE sex = 'F')",
    ]

    db = Database(db_host, db_user, db_password, db_name)

    for query in queries:
        res_sql = db.fetch(query)
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
            SaveToJson(value, 'query{}.json'.format(index)).save()
    elif output_format == 'xml':
        for index, value in enumerate(result):
            xml = dicttoxml(value).decode('utf-8')
            dom = parseString(xml)
            SaveToXml(dom, 'query{}.xml'.format(index)).save()
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
