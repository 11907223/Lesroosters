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
        self.course: str = course
        self.students: dict[str, Student] = {}
        self.category: str = category
        self.capacity: int = capacity

    def add_student(self, student) -> None:
        """Add a student to the list of students participating in activity.

        Args:
            student (Student): Student to add to activity.
        """
        self.students.update({student.index: student})

    def get_course(self, courses):
        """Return the course object of the activity.
        
        Args:
            courses (dict[str, Course]): Contains all courses.
        """
        return courses[self.course]