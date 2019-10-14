import json
from dicttoxml import dicttoxml
import xml.dom.minidom
from xml.dom.minidom import parseString


class SaveFile():
    def __init__(self, result):
        self.result = result

    def save(self):
        raise NotImplementedError


class SaveToJson(SaveFile):
    def __init__(self, result):
        super().__init__(result)

    def save(self):
        with open("result.json", "w") as write_file:
            json.dump(self.result, write_file, sort_keys=True, indent=4)


class SaveToXml(SaveFile):
    def __init__(self, result):
        super().__init__(result)

    def save(self):
        with open("result.xml", "w") as xml_file:
            self.result.writexml(xml_file, indent='\n', addindent='\t')


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


class AddData():
    def __init__(self, students, rooms):
        self.students = students
        self.rooms = rooms

    def add_students_to_rooms(self):

        for room in self.rooms:
            room['students'] = []

        dict_rooms = {room['id']: room for room in self.rooms}

        for student in self.students:
            student_room = student['room']
            student_dict = student.copy()
            student_dict.pop('room')

            try:
                dict_rooms[student_room]['students'].append(student_dict)
            except KeyError:
                print('ERROR!Wrong room id.')

        return [item for item in dict_rooms.values()]


def main(students_path, rooms_path, output_format):
    students = ReadJson(students_path).read()
    rooms = ReadJson(rooms_path).read()
    result = AddData(students, rooms).add_students_to_rooms()

    if output_format == 'json':
        SaveToJson(result).save()
    elif output_format == 'xml':
        xml = dicttoxml(result).decode('utf-8')
        dom = parseString(xml)
        SaveToXml(dom).save()
    else:
        print('Check output format')


if __name__ == "__main__":
    students_path = "students.json"
    rooms_path = "rooms.json"
    output_format = "xml"
    main(students_path, rooms_path, output_format)
