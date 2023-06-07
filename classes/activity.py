class Activity():
    """
    category = lecture, practical or workgroup.
    """

    def __init__(self, course, category, capacity, students=None) -> None:
        self.course = course
        self.students = students
        self.category = category
        self.capacity = capacity

    def add_student(self, student):
        self.students.append(student)
