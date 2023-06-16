from libraries.classes.course import Course
from libraries.classes.student import Student


class Activity:
    """ "Class containing single activity in a course.

    Possible activity categories are lecture, practical or tutorial.
    """

    def __init__(self, course, category, capacity) -> None:
        """Initialize activity for a course.

        Args:
            course (str): The course which the activity belongs to.
            category (str): The category of the activity.
                Options=lecture, tutorial or practical.
            capacity (): Maximum number of students in the activity.
            students (): List of students in the activity.
        """
        self.course: Course = course
        self.category: str = category
        self.capacity: int = capacity
