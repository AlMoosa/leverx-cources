class Solution():
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
