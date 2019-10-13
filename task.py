import json
from typing import List, Dict


def solution(students: List[Dict], rooms: List[Dict]) -> List[Dict]:
    """
    This function gets two lists with dictionaries and adds
    information about student to the field "students" in rooms.
    Returns the list with dictionaries with information about rooms.
    """

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


def main():
    """
    This function calls solution function and prints the result.
    """

    students = [
        {
            'id': 1,
            'name': 'Nikita #1',
            'room': 1
        },
        {
            'id': 2,
            'name': 'Nikita #2',
            'room': 1
        },
        {
            'id': 3,
            'name': 'Nikita #3',
            'room': 2
        },
        {
            'id': 4,
            'name': 'Nikita #4',
            'room': 2
        },
        {
            'id': 5,
            'name': 'Nikita #5',
            'room': 2
        },
        {
            'id': 6,
            'name': 'Nikita #6',
            'room': 2
        },
        {
            'id': 7,
            'name': 'Nikita #7',
            'room': 3
        }
    ]

    rooms = [
        {
            'id': 1,
            'name': 'Room #1',
            'students': []
        },
        {
            'id': 2,
            'name': 'Room #2',
            'students': []
        },
        {
            'id': 42,
            'name': 'Room #42',
            'students': []
        }
    ]

    rooms_w_students = solution(students, rooms)
    print(json.dumps(rooms_w_students, sort_keys=True, indent=4))


if __name__ == "__main__":
    main()
