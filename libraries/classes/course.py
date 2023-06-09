# from .student import Student

class Course:
    """ "Contains all information in a course."""

    def __init__(
        self,
        name,
        lectures,
        tutorials,
        max_tutorial_capacity,
        practicals,
        max_practical_capacity,
        expected,
    ) -> None:
        """Initialize the Course with the relevant information.

        Args:
            name (str): Name of the course.
            lectures (int): Number of lectures in the course.
            tutorials (int): Number of tutorials in the course.
            max_tutorials_capacity (int): Maximum number of students in a tutorial.
            practicals (int): Number of practicals in the course.
            max_practical (int): Maximum number of students in a practical.
            expected (int): Expected number of students in the course.
        """
        self.name: str = name
        self.lectures: int = lectures
        self.tutorials: int = tutorials
        self.practicals: int = practicals
        self.max_practical_capacity: int = max_practical_capacity
        self.max_tutorial_capacity: int = max_tutorial_capacity
        self.expected: int = expected
        self.students = {}

    def number_of_activities(self):
        """Return total number of activities in the course."""
        return len(self.tutorials) + len(self.practicals) + len(self.lectures)

    def all_activities(self):
        """Return all activity objects of the course."""
        return self.lectures + self.practicals + self.tutorials

    def add_student(self, student):
        self.students.update({student.index: student})