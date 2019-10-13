"""
Даны 2 файла (смотрите в прикрепленных файлах):
- students.json
- rooms.json

Необходимо написать скрипт, целью которого будет загрузка этих двух файлов,
объединения их в список комнат где каждая комната содержит список студентов
которые находятся в этой комнате, а также последующую выгрузку их в формате
JSON или XML.

Необходима поддержка следующих входных параметров:
- students # путь к файлу студентов
- rooms # путь к файлу комнат
- format # выходной формат (xml или json)
"""


from typing import List, Dict
import json
from dicttoxml import dicttoxml
import xml.dom.minidom
from xml.dom.minidom import parseString


def reading_file(file_name: str) -> List[Dict]:
    """
    This function gets the file name, opens the file
    and reads it and returns content.
    """

    try:
        with open(file_name, "r") as read_file:
            data = json.load(read_file)
        return data
    except FileNotFoundError:
        return "File {} not found!".format(file_name)


def saving_file_json(result: str):
    """
    This function gets the result and creates json file
    and then puts json content to it.
    """

    with open("result.json", "w") as write_file:
        json.dump(result, write_file, sort_keys=True, indent=4)


def saving_file_xml(result: str):
    """
    This function gets the result and creates xml file
    and then puts xml content to it.
    """

    with open("result.xml", "w") as xml_file:
        result.writexml(xml_file, indent='\n', addindent='\t')


def solution(students: List[Dict], rooms: List[Dict]) -> List[Dict]:
    """
    This function gets two lists with dictionaries and adds
    information about student to the field "students" in rooms.
    Returns the list with dictionaries with information about rooms.
    """
    for room in rooms:
        room['students'] = []

    dict_rooms = {room['id']: room for room in rooms}

    for student in students:
        student_room = student['room']
        student_dict = student.copy()
        student_dict.pop('room')

        try:
            dict_rooms[student_room]['students'].append(student_dict)
        except KeyError:
            print('ERROR!Wrong room id.')

    return [item for item in dict_rooms.values()]


def main(students_path: str, rooms_path: str, output_format: str):
    students = reading_file(students_path)
    rooms = reading_file(rooms_path)
    res = solution(students, rooms)

    if output_format == 'json':
        saving_file_json(res)
    elif output_format == 'xml':
        xml = dicttoxml(res).decode('utf-8')
        dom = parseString(xml)
        saving_file_xml(dom)
    else:
        print('Check output format')


if __name__ == "__main__":
    students_path = "students.json"
    rooms_path = "rooms.json"
    output_format = "xml"
    main(students_path, rooms_path, output_format)
