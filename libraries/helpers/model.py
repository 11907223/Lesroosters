from libraries.classes.schedule import Schedule
from libraries.classes.student import Student
from libraries.classes.course import Course
from libraries.classes.hall import Hall
from typing import Optional, Union
import copy

activity_type = tuple[Optional[str], Optional[str]]


class Model:
    def __init__(
        self,
        courses: dict[str, Course],
        students: dict[str, Student],
        halls: dict[int, Hall],
    ) -> None:
        self.courses = courses
        self.students = students
        self.halls = halls
        self.model: dict[int, activity_type] = self.init_model((None, None))
        self.participants = (
            self.init_student_model()
        )  # A model where index maps to penalty {index: penalty}
        self.index_penalties: dict[int, int] = self.init_model(
            0
        )  # A dictionary to store students, their penalty and the activities
        # that cause the penalty {student_id: [total_penalty, set(2, 140, 23)]}
        self.student_penalties: dict[int, list[Union[int, set[int]]]] = {}

    def init_model(
        self, dict_val
    ) -> dict[int, int | tuple[Optional[str], Optional[str]]]:
        """Take a Schedule object and flatten it into string representation.

        Returns:
            dict[int : dict(str, str)]: Index (0 - 144) mapping to a dict containing course and activity.
                Example: {0: {'course': 'Heuristieken', 'activity': 'lecture 1'},
                {1: {'course': None, 'activity': None}, etc.}
        """
        schedule_model: dict[int, activity_type] = {
            index: dict_val for index in range((7 * 4 + 1) * 5)
        }

        return schedule_model

    def translate_index(self, index: int) -> dict[str, int]:
        """Return index value as day, timeslot and hall indices.

        Args:
            index (int): Value 0-144 mapping to a day-hall-timeslot combination.
        """
        day = index // 29
        timeslot = (index % 29) // 7
        if (index % 29) == 28:
            # Evening slot exception.
            hall = 5
        else:
            # Regular hall indexing.
            hall = (index % 29) % 7

        return {"day": day, "timeslot": timeslot, "hall": hall}

    def init_student_model(self) -> dict[tuple[str, str], set[int]]:
        """Take the Schedule object and convert it into a activity - student dict.

        Activities are structured as a tuple('Heuristieken', 'lecture 1').

        Returns:
            dict[tuple[str, str], set[str]]:
                Activity (as unique tuple of course-activity) and a set of student indices.
        """
        participants: dict[tuple[str, str], set[int]] = {}
        for course in self.courses.values():
            for activity in course.activities():
                participants.update({(course.name, activity.category): {}})

        return participants

    def return_models(self):
        """Return schedule and activities-student dicts of strings."""
        return self.model, self.participants

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
            # Check if stored activity and index match stored information.
            check_index = self.get_index(activity)
            check_activity = self.get_activity(index)

            if check_index == index and check_activity == activity:
                # Remove activity from stored index.
                self.model[index] = (None, None)
                return True
            else:
                return False

        elif activity is not None:
            # Remove activity from stored index.
            index = self.get_index(activity)
            self.model[index] = (None, None)
            return True

        elif index is not None:
            # Remove activity from stored index.
            self.model[index] = (None, None)
            return True

        return False

    def get_hall_capacity(self, index: int) -> int:
        """Return capacity of the hall that is represented by index."""
        # Translate index into information
        info = self.translate_index(index)
        # Get the hall that is described by index
        hall_index = info["hall"]
        # Return hall capacity by from list
        return self.halls[hall_index].capacity

    def get_activity_capacity(self, activity: tuple[str, str]) -> int:
        """Return the capacity of an activity.
         
        If activity is None, return zero.
        """
        # Start with capacity 0
        capacity = 0
        # Extract course name and type from activity
        course_name = activity[0]
        type = activity[1]

        if course_name and type:
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
        else:
            # If activity is None, return 0
            return 0

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

    def student_in_course(self, student: int, course) -> bool:
        """"Return bool if student in specified course."""
        return True if student in self.courses[course] else False

    def add_student(self, student: int, activity: tuple[str, str]) -> bool:
        """Add student to an activity in the model.

        Args:
            student (int): Index id of a student.
            activity (tuple[str, str]) : tuple("course name", "lecture 1)

        Returns:
            bool: True if student not in activity yet, False otherwise.
        """
        if student not in self.participants[activity] and self.student_in_course(student, activity[0]):
            self.participants[activity].add(student)
            return True
        else:
            return False

    def remove_student(self, student: int, activity: tuple[str, str]) -> bool:
        """Remove student from an activity in the model.

        Args:
            student (int): Index id of a student.
            activity (tuple[str, str]) : tuple("course name", "lecture 1)

        Returns:
            bool: True if student succesfully removed from activity, False otherwise.
        """
        if student in self.participants[activity]:
            self.participants[activity].remove(student)
            return True
        else:
            return False

    def student_activities(self, student: int) -> dict[int, tuple[str, str]]:
        """Return a dict of activities and schedule indices of the student.

        Args:
            student (int): Index id of the student.
        """
        activity_set = {
            activity
            for activity, student_list in self.participants.items()
            if student in student_list
        }
        index_set = {
            index for index, activity in self.model.items() if activity in activity_set
        }
        return dict(zip(index_set, activity_set, strict=True))

    def get_highest_penalties(self, n) -> list[list[Union[int, tuple[str, str]]]]:
        """Search the schedule for activities with highest penalties.
        Returns a list of length n where each element represents an activity that
        caused a high penalty, this element is also a list which contains a tuple with course name
        and activity type, and the index. The first element (list[0])
        is the activty with the highest penalty and the last element (list[n]) is the
        activity with the lowest penalty.

        returns: list[list[index: int, activity: tuple[str, str]]]"""

        # Run total_penalty() to update self.index_penalties
        self.total_penalty()

        # Initialize an empty list
        highest_penalties = []
        # Take the penalty model
        model = self.index_penalties
        # Find highest penalties in de model
        highest_values = sorted(model.values(), reverse=True)[:n]

        # Iterate over the highest values
        for high_value in highest_values:
            # Iterate over model
            for index, value in model.items():
                if value == high_value:
                    # Add index and activity to list
                    activity = self.get_activity(index)
                    highest_penalties.append([index, activity])

        return highest_penalties

    def get_highest_students(self, n) -> list[int]:
        """Search the model for students in activities with highest penalties.
        Returns a list of length n where each element is the student_index of a
        student that caused a high penalty. The first element (list[0])
        is the activty with the highest penalty and the last element (list[n]) is the
        activity with the lowest penalty.

        returns: list[int]"""
        pass

    def capacity_penalty(self, index: int, activity: tuple[str, str]) -> int:
        # Get hall capacity for slot
        hall_capacity = self.get_hall_capacity(index)
        # Get activity capacity for slot
        activity_capacity = self.get_activity_capacity(activity)

        if activity_capacity > hall_capacity:
            # Return penalty points for each student over capacity.
            return activity_capacity > hall_capacity
        # Return no added penalty points.
        return 0

    def total_capacity_penalties(self) -> int:
        """Check if the number of students of each activity exceeds
        the hall capacity.For every student that doesn't fit 1 penalty
        point is counted. the total capacity penalty is returned (int).
        The function also keeps track of the model in self.index_penalties."""

        penalty_points = 0

        # Iterate over all indices in model
        for index, activity in self.model.items():
            index_penalty = self.capacity_penalty(index, activity)
            penalty_points += index_penalty
            self.index_penalties[index] += index_penalty

        print("capacity penalty:", penalty_points)
        return penalty_points

    def evening_penalty(self) -> int:
        """Calculate penalties of activities in evening slot.
        Fills in empty model with {index: penalty}.
        returns total evening penalty."""

        # Start with 0 penalty points, set evening penalty to 5
        penalty_points = 0
        evening_penalty = 5

        # Iterate over indices and activities in model
        for index, activity in self.model.items():
            # If index is mapped to activity
            if activity[0]:
                # Get info on index
                info = self.translate_index(index)
                # Check if activity is in evening slot
                if info["timeslot"] == 4:
                    # If so, add penalty points
                    penalty_points += evening_penalty
                    self.index_penalties[index] += evening_penalty

        print("evening penalty:", penalty_points)
        return penalty_points

    def conflict_penalty(self) -> int:
        """Calculate the penalties of students with course conflicts.
        Fills in empty student activity model {activity: {student_id: penalty}}.
        returns total conflict penalty. The function also keeps track of the model in
        self.student_penalties."""

        penalty_points = 0

        # Iterate over students
        for id in self.students.keys():
            # Variable for previous activities of student
            prev_slots = []
            # Total penalty points of student
            student_penalty = 0
            # Get all activities from student
            activities = self.student_activities(int(id))
            # Iterate over activites
            for activity in activities:
                # Get info on activity
                info = self.translate_index(activity)
                # Save day-timeslot
                temp = (info["timeslot"], info["day"])
                # Check if day-timeslot was already used for other activity
                if temp in prev_slots:
                    # If so, update student penalty and total penalty
                    student_penalty += 1
                    penalty_points += 1
                    # If student is not in student penalty model
                    if id not in self.student_penalties.keys():
                        # Add student to model
                        self.student_penalties.update(
                            {id: [student_penalty, {activity}]}
                        )
                    # If student already in model
                    else:
                        # Update student penalty and add activity index
                        self.student_penalties[id][0] = student_penalty
                        self.student_penalties[id][1].add(activity)
                # If day-timeslot not used
                else:
                    # add to previous slot variable
                    prev_slots.append(temp)

        print("conflict penalty: ", penalty_points)

        return penalty_points

    def schedule_gaps_penalty(self) -> int:
        """Calculates The function also keeps track of the model in
        self.student_penalties."""
        pass

    def total_penalty(self) -> int:
        """Calculates the total penalty of the schedule.

        return: penalty (int)"""
        total = (
            self.total_capacity_penalties() + self.evening_penalty() + self.conflict_penalty()
        )

        return total

    def copy(self) -> 'Model':
        new_copy = copy.copy(self)
        new_copy.model = copy.copy(self.model)
        new_copy.participants = copy.copy(self.participants)
        
        return new_copy