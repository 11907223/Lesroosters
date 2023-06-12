class Activity:
    """ "Class containing single activity in a course.

    Possible activity categories are lecture, practical or tutorial.
    """

    def __init__(self, course, category, capacity) -> None:
        """Initialize activity for a course.

        Args:
            course (): The course which the activity belongs to.
            category (): The category of the activity.
                Options: (lecture, tutorial or practical).
            capacity (): The maximum number of students in the activity.
            students (): The list of students in the activity.
        """
        self.course = course
        self.students = {}
        self.category = category
        self.capacity = capacity

    def add_student(self, student) -> None:
        """Add a student to the list of students participating in activity.

        Args:
                student (): Student to include in course activity.
        """
        self.students.update({student.index: student})
