CREATE TABLE Rooms (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(10) NOT NULL
);

CREATE TABLE Students (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    room INT,
    birthday DATETIME NOT NULL,
    sex CHAR(1) CHECK(sex IN ('M','F')),
    FOREIGN KEY (room) REFERENCES Rooms (id) ON DELETE SET NULL
);


SELECT Rooms.name AS ROOM_NAME, COUNT(room) AS NUM_OF_STUDENTS FROM Students INNER JOIN Rooms ON Rooms.id = Students.room GROUP BY room;
SELECT Rooms.name AS ROOM, AVG((TO_DAYS(NOW())-TO_DAYS(birthday))/365) AS AVG_AGE FROM Students INNER JOIN Rooms ON Rooms.id = Students.room GROUP BY Rooms.name ORDER BY AVG_AGE LIMIT 5;
SELECT Rooms.name AS ROOM, ((MAX((TO_DAYS(NOW())-TO_DAYS(birthday)))- MIN((TO_DAYS(NOW())-TO_DAYS(birthday))))/365) AS DIFF FROM Students INNER JOIN Rooms ON Rooms.id = Students.room GROUP BY Rooms.name ORDER BY DIFF DESC LIMIT 5;
SELECT Rooms.name FROM Rooms INNER JOIN Students ON Students.room = Rooms.id GROUP BY Rooms.id HAVING COUNT(DISTINCT Students.sex)>=2;
