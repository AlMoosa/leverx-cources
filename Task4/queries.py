from dbconnectors import DatabaseConnector, MySqlConnector


def deleting_tables():
    queries = (
        'DROP TABLE Students',
        'DROP TABLE Rooms'
    )

    return queries


def creating_tables():
    queries = (
        """
        CREATE TABLE Rooms (
            id INT NOT NULL PRIMARY KEY,
            name VARCHAR(10) NOT NULL
        );
        """,
        """
        CREATE TABLE Students (
            id INT NOT NULL PRIMARY KEY,
            name VARCHAR(30) NOT NULL,
            room INT,
            birthday DATETIME NOT NULL,
            sex CHAR(1) CHECK(sex IN ('M','F')),
            FOREIGN KEY (room) REFERENCES Rooms (id) ON DELETE SET NULL
        );
        """
    )

    return queries


def selecting_data_from_db():
    queries = {
        'rooms_with_the_num_of_students': [
            """
            SELECT Rooms.name AS ROOM_NAME, COUNT(room) AS NUM_OF_STUDENTS
            FROM Students INNER JOIN Rooms ON Rooms.id = Students.room
            GROUP BY room
            """,
            None
        ],
        'top5_rooms_with_min_avg_age': [
            """
            SELECT Rooms.name AS ROOM, AVG((TO_DAYS(NOW())-TO_DAYS(birthday))/365) AS AVG_AGE
            FROM Students INNER JOIN Rooms ON Rooms.id = Students.room
            GROUP BY Rooms.name
            ORDER BY AVG_AGE
            LIMIT 5
            """,
            None
        ],
        'top5_rooms_with_max_age_difference': [
            """
            SELECT Rooms.name AS ROOM, ((MAX((TO_DAYS(NOW())-TO_DAYS(birthday)))- MIN((TO_DAYS(NOW())-TO_DAYS(birthday))))/365) AS DIFF
            FROM Students INNER JOIN Rooms ON Rooms.id = Students.room
            GROUP BY Rooms.name
            ORDER BY DIFF DESC
            LIMIT 5
            """,
            None
        ],
        'rooms_with_different_sex': [
            """
            SELECT Rooms.name
            FROM Rooms INNER JOIN Students ON Students.room = Rooms.id
            GROUP BY Rooms.id
            HAVING COUNT(DISTINCT Students.sex)>=2
            """,
            None
        ]
    }

    return queries


def inserting_data_to_db():
    queries = {
        'rooms': 'INSERT INTO Rooms (id,name) VALUES (%s,%s)',
        'students': 'INSERT INTO Students (id,name,room,birthday,sex) VALUES (%s,%s,%s,%s,%s)'
    }

    return queries


def executing_queries(students, rooms, db_host, db_user, db_password, db_name):

    with MySqlConnector(db_host, db_user, db_password, db_name) as db:

        delete_queries = deleting_tables()
        for item in delete_queries:
            db.execute(item)

        сreate_queries = creating_tables()
        for item in сreate_queries:
            db.execute(item)

        insert_queries = inserting_data_to_db()
        for room in rooms:
            db.execute(
                insert_queries['rooms'],
                (room['id'], room['name'])
            )
        for student in students:
            db.execute(
                insert_queries['students'],
                (student['id'], student['name'], student['room'],
                 student['birthday'], student['sex'])
            )

        select_queries = selecting_data_from_db()
        for value in select_queries.values():
            value[1] = db.query(value[0])

    return select_queries
