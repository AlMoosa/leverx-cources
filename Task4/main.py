from cli import parser
from filereaders import FileReader, JsonReader
from filesavers import FileSaver, JsonSaver, XmlSaver
from queries import executing_queries


def main(students_path, rooms_path, output_format,
         db_host, db_user, db_password, db_name):

    rooms = JsonReader(rooms_path).read()
    students = JsonReader(students_path).read()

    result = executing_queries(
        students, rooms, db_host, db_user, db_password, db_name)

    if output_format == 'json':
        for key, value in result.items():
            JsonSaver(value[1], '{}.json'.format(key)).save()
    elif output_format == 'xml':
        for key, value in result.items():
            XmlSaver(value[1], '{}.xml'.format(key)).save()
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
