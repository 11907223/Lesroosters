from course import Course


class Student:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        id: int,
        courses: list[Course],
    ) -> None:
        """Initialize the Course with the relevant information.

        Args:
            first_name (str): Student first name.
            last_name (str): Student last name.
            id (int): Student ID number .
            courses (list[Course]): Enrolled courses of the student.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        self.courses = courses
