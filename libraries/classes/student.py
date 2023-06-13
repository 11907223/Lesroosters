from typing import TYPE_CHECKING
from libraries.classes.course import Course
if TYPE_CHECKING:
    from libraries.classes.activity import Activity

class Student:
    def __init__(
        self,
        index: int,
        first_name: str,
        last_name: str,
        student_number: int,
        courses: dict[str,Course],
    ) -> None:
        """Initialize the Course with the relevant information.

        Args:
            index (int): Index of student in file.
            first_name (str): Student first name.
            last_name (str): Student last name.
            student_number (int): Student ID number.
            courses (list[Course]): Enrolled courses of the student.
        """
        self.index: int = index
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.student_number: int = student_number
        self.courses: dict[str, Course] = courses
        self.activites: dict[str, Activity] = {}

    def add_course(self, course: Course):
        self.courses.update({course.name: course})

    def add_activity(self, activity):
        self.activities.update({f"{activity.course.name} {activity.name}": activity})