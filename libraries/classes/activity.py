class Activity:
    """ "Class containing single activity in a course.

    Possible activity categories are lecture, practical or tutorial.
    """

    def __init__(self, course, category, capacity, students=None) -> None:
        """Initialize activity for a course.

        Args:
            course (): The course to which the membership belongs.
            category (): The category of the membership.
            capacity (): The capacity of the membership.
            students (): The list of students in the course.
        """
        self.course = course
        self.students = students
        self.category = category
        self.capacity = capacity

    def add_student(self, student) -> None:
        """Add a student to the list of students participating in activity.

        Args:
                student (): Student to include in course activity.
        """
        self.students.append(student)
