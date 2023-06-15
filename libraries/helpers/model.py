from libraries.classes.schedule import Schedule
from libraries.classes.student import Student
from libraries.classes.course import Course
from typing import Optional


activity_type = tuple[Optional[str], Optional[str]]


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
        self.model: dict[int, activity_type] = self.init_model()
        self.activities = self.init_student_model()
        # A model where index maps to penalty {index: penalty}
        self.index_penalties = {}
        # A dictionary to store students, their penalty and the activities
        # that cause the penalty {student_id: [total_penalty, set(2, 140, 23)]}
        self.student_penalties: dict[int, list[int, set[int]]] = {}

    def init_model(self) -> dict[int, tuple[Optional[str], Optional[str]]]:
        """Take a Schedule object and flatten it into string representation.

        Returns:
            dict[int : dict(str, str)]: Index (0 - 144) mapping to a dict containing course and activity.
                Example: {0: {'course': 'Heuristieken', 'activity': 'lecture 1'},
                {1: {'course': None, 'activity': None}, etc.}

        """
        schedule_model: dict[int, activity_type] = {}
        for index, entry in enumerate(self.schedule.as_list_of_dicts()):
            activity: str = entry["activity"]
            course: str = entry["course"]
            schedule_model[index] = (
                course,
                activity,
            )

        return schedule_model

    def translate_index(self, index: int) -> dict[str, int]:
        """Return index value as day, timeslot and hall indices.

        Args:
            index (int): Value 0-144 mapping to a day-hall-timeslot combination.
        """
        day = index // (5 * (7 - 1))
        timeslot = index % 5
        # Assymetry requires an if statement for the evening slot.
        if index // 5 < 28:
            hall = (index // 5) % 7
        else:
            hall = 5

        return {"day": day, "timeslot": timeslot, "hall": hall}

    def init_student_model(self) -> dict[tuple[str, str], set[str]]:
        """Take the Schedule object and convert it into a activity - student dict.

        Activities are structured as a tuple('Heuristieken', 'lecture 1').

        Returns:
            dict[tuple[str, str], set[str]]:
                Activity (as unique tuple of course-activity) and a set of student indices.
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

    def check_index_is_empty(self, index: int) -> bool:
        """Return a boolean indicating if index slot contains a course-activity pair."""
        return self.model[index][0] is None

    def add_activity(self, index: int, activity: tuple[str, str]) -> bool:
        """Add activity to given index in schedule model.

        Returns:
            bool: True if activity was succesfully added, else False.
        """
        if self.check_index_is_empty(index) is True:
            self.model[index] = activity
            return True
        else:
            return False

    def remove_activity(
        self,
        activity: Optional[activity_type] = None,
        index: Optional[int] = None,
    ) -> bool:
        """Remove activity from the schedule model.

        Activities are structured as tuple("course name", "lecture 1).

        If only activity is given, index is searched and activity is removed at found index.
        If only index is given, activity at specified index is removed.
        If both are given, given activity is compared to stored activity before removal.

        Args:
            activity (tuple[str, str]): course name, activity type.
                Example: ("Heuristieken", "lecture 1)
            index (int): Index in schedule, ranging from 0 - 144.

        Returns:
            bool: True if activity was succesfully removed,
                False if nothing to remove or given activity does not match stored activity.
        """
        if activity is not None and index is not None:
            check_index = self.get_index(activity)
            check_activity = self.get_activity(index)

            if check_index == index and check_activity == activity:
                self.model[index] = (None, None)
                return True
            else:
                return False

        elif activity is not None:
            index = self.get_index(activity)
            self.model[index] = (None, None)
            return True

        elif index is not None:
            self.model[index] = (None, None)
            return True

        return False

    def get_hall_capacity(self, index: int) -> int:
        """Return capacity of the hall that is represented by index."""
        # List of the capacity of all lecture halls
        halls_capacity = [41, 22, 20, 56, 48, 117, 60]
        # Translate index into information
        info = self.translate_index(index)
        # Get the hall that is described by index
        hall_index = info["hall"]
        # Return hall capacity by from list
        return halls_capacity[hall_index]

    def get_activity_capacity(self, activity: tuple[str, str]) -> int:
        """Returns capacity of an activity."""
        # Start with capacity 0
        capacity = 0
        # Extract course name and type from activity
        course_name = activity[0]
        type = activity[1]

        # Find the course object the activity belongs to
        course = self.courses[course_name]
        # Combine all course activities in one list
        all_activities = course.lectures + course.practicals + course.tutorials

        # Iterate over all Activity objects
        for object in all_activities:
            # If type matches Activity category
            if type == object.category:
                # Set capacity
                capacity = object.capacity

        return int(capacity)

    def get_index(self, activity: tuple[str, str]) -> int:
        """Return index of activity in model.

        Args:
            activity (tuple[str, str]): ('course name', 'lecture 1')
        """
        return {index for index in self.model if self.model[index] == activity}.pop()

    def get_activity(self, index: int) -> activity_type:
        """Return activity stored at index in model.

        Args:
            index (int): Value ranging from 0 - 144
        """
        return self.model[index]

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
        # Start counting at 0 penalty points
        penalty_points = 0

        return penalty_points

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
        """Calculates the total penalty of the schedule.

        return: penalty (int)"""
        total = (
            self.capacity_penalty() + self.evening_penalty() + self.conflict_penalty()
        )
        return total
