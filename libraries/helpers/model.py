from libraries.classes.schedule import Schedule
from libraries.classes.student import Student
from libraries.classes.course import Course


class Model:
    def __init__(
        self,
        courses: dict[str, Course],
        students: dict[str, Student],
        schedule: Schedule,
    ) -> None:
        self.courses = courses
        self.students = students
        self.schedule = schedule
        self.model = self.get_empty_model()
        self.activities = self.empty_student_model()
        # A model where index maps to penalty {index: penalty}
        self.index_penalties = {}
        # A dictionary to store students, their penalty and the activities
        # that cause the penalty {student_id: [total_penalty, set(2, 140, 23)]}
        self.student_penalties: dict[int, list[int, set[int]]] = {}

    def get_empty_model(self) -> dict[int, dict[str, str]]:
        """Take a Schedule object and flatten it into string representation.

        Returns:
            dict[int : dict(str, str)]: Index (0 - 144) mapping to a dict containing course and activity.
                Example: {0: {'course': 'Heuristieken', 'activity': 'lecture 1'}, 
                {1: {'course': None, 'activity': None}, etc.}

        """
        schedule_model = {}
        for index, entry in enumerate(self.schedule.as_list_of_dicts()):
            activity: str = entry["activity"]
            course: str = entry["course"]
            schedule_model[index] = {
                "course": course,
                "activity": activity,
            }

        return schedule_model

    def translate_index(self, index: int) -> dict[str, int]:
        """Return index value as day, timeslot and hall indices.

        Args:
            index (int): Value 0-144 mapping to a day-hall-timeslot combination.
        """
        day = index // (5 * (7 - 1))
        timeslot = index % 5
        hall = (index // 5) % (7 - 1)

        return {"day": day, "timeslot": timeslot, "hall": hall}

    def empty_student_model(self) -> dict[tuple[str, str], str]:
        """Take the Schedule object and convert it into a Student and Activity dictionary.

        Activities are structured as a tuple("course name", "lecture 1).

        Returns:
            dict[tuple[str, str], set[str]]:
        """
        students_in_activities = {}
        for day in self.schedule.days.values():
            for slot in day.slots:
                if slot.activity is not None:
                    student_set = set()
                    for student in slot.activity.students:
                        student_set.add(student)
                    students_in_activities.update(
                        {
                            (
                                slot.activity.course.name,
                                slot.activity.category,
                            ): student_set
                        }
                    )

        return students_in_activities

    def return_models(self):
        """Return schedule and activities-student dicts of strings."""
        return self.model, self.activities

    def add_activity(self, index: int, activity: tuple[str, str]) -> bool:
        """Add activity to given index in schedule model.

        Returns:
            bool: True if activity was succesfully added.
        """
        pass

    def remove_activity(self, activity: tuple[str, str], index: int) -> bool:
        """removes activity to given index in schedule model. Function returns True if
        activity was succesfully removed.

        Activities are structured as follows tuple("course name", "lecture 1)
        """
        pass

    def get_capacity(self, index: int) -> int:
        """Returns capacity of the hall that is represented by index."""
        pass

    def get_index(self, activity: tuple[str, str]) -> int:
        """Get model index of activity. Activities should be
        structured as tuple("course name", "lecture 1)"""
        pass

    def add_student(self, student: int, activity: tuple[str, str]) -> bool:
        """Add student to student-activity model. Activities should be
        structured as tuple("course name", "lecture 1). Students are
        represented by their index (int)"""
        pass

    def remove_student(self, student: int, activity: tuple[str, str]) -> bool:
        """Remove student to student-activity model. Activities should be
        structured as tuple("course name", "lecture 1). Students are
        represented by their index (int)"""
        pass

    def student_activities(self, student: int) -> list[int]:
        """Returns list of activities that the student is assigned to.
        The list contains the indices (int) of activities in the schedule."""
        pass

    def get_highest_penalties(self, n) -> list[list[tuple[str, str], int]]:
        """Searches the schedule for activities with highest penalties.
        Returns a list of length n where each element represents an activity that
        caused a high penalty, this element is a list which contains a tuple with course name
        and activity type, and the index. The first element (list[0])
        is the activty with the highest penalty and the last element (list[n]) is the
        activity with the lowest penalty.

        returns: list[list[activity: tuple[str, str], index: int]]"""
        pass

    def get_highest_students(self, n) -> list[int]:
        """Searches the model for students in activities with highest penalties.
        Returns a list of length n where each element is the student_index of a
        student that caused a high penalty. The first element (list[0])
        is the activty with the highest penalty and the last element (list[n]) is the
        activity with the lowest penalty.

        returns: list[int]"""
        pass

    def capacity_penalty(self) -> int:
        """Checks if the number of students of each activity exceeds
        the hall capacity.For every student that doesn't fit 1 penalty
        point is counted. the total capacity penalty is returned (int).
        The function also keeps track of the model in self.index_penalties."""

        pass

    def evening_penalty(self) -> int:
        """Calculate penalties of activities in evening slot.
        Fills in empty model with {index: penalty}.
        returns total evening penalty."""
        pass

    def conflict_penalty(self) -> int:
        """Calculates penalties of students with course conflicts.
        Fills in empty student activity model {activity: {student_id: penalty}}.
        returns total conflict penalty. The function also keeps track of the model in
        self.student_penalties."""
        pass

    def total_penalty(self) -> int:
        total = (
            self.capacity_penalty()
            + self.evening_penalty()
            + self.conflict_penalty()
        )
        return total
