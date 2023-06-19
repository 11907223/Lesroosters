from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from libraries.classes.student import Student
    from libraries.classes.activity import Activity


class Course:
    """ "Contains all information in a course.

    Attributes:
        name (str) : Name of the course (e.g. Heuristieken 1).
        lectures (list[Activity]): List of lecture Activity objects in the course.
        tutorials (list[Activity]): List of tutorial Activity objects in the course.
        practicals (list[Activity]): List of practical Activity objects in the course.
        students (dict[str, Student]): Mapping of student indices to Student objects.
    """

    def __init__(self, course_name) -> None:
        """Initialize the Course with the relevant information.

        Args:
            course_name (str): Name of the course.

        """
        self.name: str = course_name
        self.lectures: list[Activity] = []
        self.tutorials: list[Activity] = []
        self.practicals: list[Activity] = []
        self.students: dict[str, Student] = {}

    def add_activity(self, type: str, activity) -> bool:
        if type == "lectures":
            self.lectures.append(activity)
            return True
        if type == "tutorials":
            self.tutorials.append(activity)
            return True
        if type == "practicals":
            self.practicals.append(activity)
            return True
        else:
            return False

    def number_of_activities(self):
        """Return total number of activities in the course."""
        return len(self.tutorials) + len(self.practicals) + len(self.lectures)

    def activities(self):
        """Return all activity objects of the course."""
        return self.lectures + self.practicals + self.tutorials

    def add_student(self, student):
        self.students.update({student.index: student})
