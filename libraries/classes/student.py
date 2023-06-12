from .course import Course


class Student:
    def __init__(
        self,
        index: int,
        first_name: str,
        last_name: str,
        student_number: int,
        courses: Course,
    ) -> None:
        """Initialize the Course with the relevant information.

        Args:
            index (int): Index of student in file.
            first_name (str): Student first name.
            last_name (str): Student last name.
            id (int): Student ID number.
            courses (list[Course]): Enrolled courses of the student.
        """
        self.index: int = index
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.student_number: int = student_number
        self.courses: dict[str, Course] = courses
        self.activites = {}

    def add_course(self, course: Course):
        self.courses.update({course.name: course})

    def add_activity(self, activity):
        self.activities.update({f"{activity.course.name} {activity.name}": activity})