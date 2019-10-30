from cli import parser
from filereaders import FileReader, JsonReader
from filesavers import FileSaver, JsonSaver, XmlSaver
from solution import Solution


def main(students_path, rooms_path, output_format):
    students = JsonReader(students_path).read()
    rooms = JsonReader(rooms_path).read()
    result = Solution(students, rooms).add_students_to_rooms()

    if output_format == 'json':
        JsonSaver(result).save()
    elif output_format == 'xml':
        XmlSaver(result).save()
    else:
        print('Check output format')


if __name__ == "__main__":
    args = parser()

    students_path = args.path1
    rooms_path = args.path2
    output_format = args.format

    main(students_path, rooms_path, output_format)
