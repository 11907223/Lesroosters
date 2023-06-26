from __future__ import annotations
from libraries.classes.student import Student
from libraries.classes.course import Course
from libraries.classes.hall import Hall
from libraries.helpers.load_data import load_courses, load_students, load_halls
from typing import Optional
from collections import defaultdict
import numpy as np
import copy
import random


class Model:
    """A model representation for a schedule.

    Contains methods for manipulation of data in schedule indices and manipulation of members of activities.

    Attributes:
        courses (dict[str, Course]): A mapping of a course name to a Course object.
        students (dict[str, Student]):
            A mapping of a student index (based on loading order) to a Student object.
        halls (dict[str, Hall]):
            A mapping of a hall index (based on loading order) to a Hall object.
        solution (dict[int, tuple[str, str]]): A mapping of a schedule slot index
            (which maps to day-timeslot-hall) to an activity.
            An activity is represented as ('Course name', 'Activity').
            Example of an activity: ('Heuristieken 1', 'lecture 1').
        activity_enrollments (dict[tuple[str, str], set[int]]):
            A dictionary containing activities and their set of students.
            Students are represented by their index number.
        penalty_per_index (dict[int, int]): Dictionary of penalty points per index.
            E.G. {'(timeslot) 0': 5 (penalty points)}.
        penalties_per_student (dict[int, dict[int, dict[str, int]]]):
            A mapping of student IDs to a dict of days which map to the conflict penalties and gap penalties.
            Example: {(student) 0: {(day) 0: conflict penalties : 5, gap penalties : 2}.
        unassigned_activities (list[tuple[str, str]]):
            A list of activities which have not been placed in the solution.
        penalty_points (int | float): Number of penalty points added together.
            Defaults to infinite on an empty model and is overwritten when model is filled.
    """

    def __init__(self, path: str = "data", auto_load_students: bool = True) -> None:
        """Initiatizes a model for a schedule.

        Args:
            path (str): Path for data to load. Defaults to "data".
            auto_load_students (bool): evaluate if  students have to be added to
                their respective activities in initialisation. Defaults to True.
        """
        self.courses: dict[str, Course] = load_courses(path)
        self.students: dict[int, Student] = load_students(self.courses, path)
        self.halls: dict[int, Hall] = load_halls(path)
        self.solution = self.init_model((None, None))
        self.activity_enrollments: dict[
            tuple[str, str], set[int]
        ] = self.init_student_model()
        self.penalty_per_index: dict[int, int] = self.init_model(0)
        self.penalties_per_student: dict[int, dict[int, dict[str, int]]] = defaultdict(
            dict
        )
        self.unassigned_activities: tuple[str, str] = list(
            self.activity_enrollments.keys()
        )

        # Initiate an empty model with an improbably high score to ensure it always evaluates
        #   worse vs. other models. As an empty model contains no data,
        #   it can score no negative points and therefore would compare as better than
        #   a generated model.
        self.penalty_points: int | float = float("inf")

        if auto_load_students is True:
            # Add members to activities in self.participants.
            self.add_all_students_to_activities()

    def init_model(
        self, dict_value: int | tuple[Optional[str], Optional[str]]
    ) -> dict[int, int | tuple[Optional[str], Optional[str]]]:
        """Initiate a string representation of a schedule.

        Returns:
            dict[int : dict(str, str)]: 
                Index (0 - 144) mapping to a dict containing course and activity.
                Example: {0: {'course': 'Heuristieken', 'activity': 'lecture 1'},
                {1: {'course': None, 'activity': None}, etc.}
        """
        schedule_model: dict[int, int | tuple[str, str]] = {
            index: dict_value for index in range((7 * 4 + 1) * 5)
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
        """Initiate an activity mapping to a set of students.

        Activities are structured as a tuple('Heuristieken', 'lecture 1').

        Returns:
            dict[tuple[str, str], set[str]]:
                Activity (as unique tuple of course-activity) and a set of student indices.
        """
        participants: dict[tuple[str, str], set[int]] = {}
        for course in self.courses.values():
            for activity in course.activities():
                participants.update({(course.name, activity.category): set()})

        return participants

    def add_all_students_to_activities(self) -> None:
        """Add all students to activities."""
        for activity_tuple in self.activity_enrollments:
            for student in self.students:
                self.add_student_to_activity(int(student), activity_tuple)

    def get_random_index(
        self, empty: bool = False, weights: Optional(list[int]) = None
    ) -> int:
        """Return random empty index in the schedule.

        Args:
            empty (bool): Flag if random index has to be empty.
                Defaults to false.
        """
        while True:
            # Acquire index independent of content in index.
            index = random.choices(list(self.solution.keys()), weights)[0]
            if empty is False:
                # Return first found index if slot content is irrelevant.
                return index
            if self.check_index_is_empty(index) and empty is True:
                return index

    def get_high_capacity_empty_index(self) -> int:
        """Return empty index in the schedule with highest capacity."""
        capacity = 0
        highest_index = 0

        for index in self.solution:
            info = self.translate_index(index)
            temp_capacity = self.halls[info["hall"]].capacity
            if self.check_index_is_empty(index) and temp_capacity > capacity:
                capacity = temp_capacity
                highest_index = index

        return highest_index

    def check_index_is_empty(self, index: int) -> bool:
        """Return a boolean indicating if index slot contains a course-activity pair."""
        return self.solution[index][0] is None

    def get_index_penalty_dict(self) -> dict[int, int]:
        return self.penalty_per_index

    def swap_activities(self, index_1, index_2) -> None:
        """Swap activities stored at two indices.

        Args:
            index_1 (int): Index of first activity to be swapped.
            index_2 (int): Index of second activity to be swapped.
        """
        self.solution[index_1], self.solution[index_2] = (
            self.solution[index_2],
            self.solution[index_1],
        )

    def add_activity(self, index: int, activity: tuple[str, str]) -> bool:
        """Add activity to given index in schedule model.

        Returns:
            bool: True if activity was succesfully added, else False.
        """
        if self.check_index_is_empty(index) is True:
            self.solution[index] = activity
            return True
        else:
            return False

    def remove_activity(
        self,
        activity: Optional[tuple[str, str]] = None,
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
            check_index = self.get_index_of_activity(activity)
            check_activity = self.get_activity_of_index(index)

            if check_index == index and check_activity == activity:
                # Remove activity from stored index.
                self.solution[index] = (None, None)
                return True
            else:
                return False

        elif activity is not None:
            # Remove activity from stored index.
            index = self.get_index_of_activity(activity)
            self.solution[index] = (None, None)
            return True

        elif index is not None:
            # Remove activity from stored index.
            self.solution[index] = (None, None)
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

    def get_student_count_in_activity(self, activity: tuple[str, str]) -> int:
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
                    capacity = len(self.activity_enrollments[(course_name, type)])

            return int(capacity)
        else:
            # If activity is None, return 0
            return 0

    def get_index_of_activity(self, activity: tuple[str, str]) -> int:
        """Return index of activity in model.

        Args:
            activity (tuple[str, str]): ('course name', 'lecture 1')
        """
        return {
            index for index in self.solution if self.solution[index] == activity
        }.pop()

    def get_activity_of_index(self, index: int) -> tuple[str, str]:
        """Return activity stored at index in model.

        Args:
            index (int): Value ranging from 0 - 144
        """
        return self.solution[index]

    def check_student_in_course(self, student: int, course) -> bool:
        """Return bool if student in specified course."""
        return True if student in self.courses[course].students else False

    def add_student_to_activity(self, student: int, activity: tuple[str, str]) -> bool:
        """Add student to an activity in the model.

        Args:
            student (int): Index id of a student.
            activity (tuple[str, str]) : tuple("course name", "lecture 1)

        Returns:
            bool: True if student not in activity yet, False otherwise.
        """
        if student not in self.activity_enrollments[
            activity
        ] and self.check_student_in_course(student, activity[0]):
            self.activity_enrollments[activity].add(student)
            return True
        else:
            return False

    def get_student_schedule(self, student: int) -> dict[int, tuple[str, str]]:
        """Return a dict of schedule and activities of the student.

        Example: {0: (Heuristieken, lecture 1), 1: (Algoritmes, werkcollege 1)}

        Args:
            student (int): Index id of the student.
        """
        activities = [
            activity
            for activity, student_list in self.activity_enrollments.items()
            if student in student_list
        ]
        activity_and_indices: dict[int, tuple[str, str]] = {
            index: activity
            for index, activity in self.solution.items()
            if activity in activities
        }
        return activity_and_indices

    def get_penalties_per_day(self, type="str") -> dict[int, dict[str, int]]:
        """Return a dictionary of conflict and gap penalty of each day."""
        penalty_per_day: dict[int, dict[str, int]] = {i: 0 for i in range(5)}
        for student_penalty in self.penalties_per_student.values():
            for day, penalties in student_penalty.items():
                for penalty_type, penalty_value in penalties.items():
                    if penalty_type == type:
                        penalty_per_day[day] += penalty_value

        return penalty_per_day

    def get_worst_days(self) -> dict[str, int]:
        """Return the day of highest gap penalties and the day of highest conflict penalties."""
        gap_per_day = self.get_penalties_per_day("gap penalties")
        conflict_per_day = self.get_penalties_per_day("conflict penalties")

        worst_gap_day = max(gap_per_day, key=gap_per_day.get)
        worst_conflict_day = max(conflict_per_day, key=conflict_per_day.get)

        return {"gap day": worst_gap_day, "conflict day": worst_conflict_day}

    def get_penalty_extremes(
        self, n: int, highest: bool = True
    ) -> dict[int, tuple[str, str]]:
        """Form a list of activities with highest contributions to penalty points.

        The list of elements is ordered from activities causing most to least penalty points.
        The activities are stored in a dict mapping from their index to the activity.

        Args:
            n (int): length of the list to return.
            highest (bool): Evaluate if best or worst scorers are returned.

        Returns:
            dict[int, tuple[str, str]]]: A dictionary of {index: activity}
                E.g. {0: ('Heuristieken': 'lecture 1')}.
        """

        # Update self.index_penalties.
        self.calc_total_penalty()

        # Find the highest penalties stored.
        highest_penalties = {}
        model = self.penalty_per_index
        highest_values = sorted(model.values(), reverse=highest)[:n]

        for high_value in highest_values:
            for index, value in model.items():
                if value == high_value:
                    activity = self.get_activity_of_index(index)
                    highest_penalties.update({index: activity})

        return highest_penalties

    def calc_capacity_penalty_at_(self, index: int, activity: tuple[str, str]) -> int:
        """Return the capacity penalty for an activity over capacity.

        Args:
            index (int): Index of the activity in the model.
            activity (tuple[str, str]): Activity to check,
                an activity is a tuple of ('course name', 'activity').

         Returns:
            int: Penalty points for each student over capacity. 0 if there is no penalty.
        """
        # Get capacity for the activity and the location.
        hall_capacity = self.get_hall_capacity(index)
        activity_capacity = self.get_student_count_in_activity(activity)

        if activity_capacity > hall_capacity:
            # Return penalty points for each student over capacity.
            return activity_capacity - hall_capacity
        # Return no penalty points.
        #   Ensure that penalty points are not subtracted.
        return 0

    def calc_total_capacity_penalties(self) -> int:
        """Check the capacity penalty per index.

        For every student student in an activity that exceeds the hall capacity
            1 penalty point is counted.
        Additionally penalties are stored in  self.index_penalties.

        Returns:
            int: The sum of all capacity penalties.
        """
        penalty_points = 0

        for index, activity in self.solution.items():
            index_penalty = self.calc_capacity_penalty_at_(index, activity)
            penalty_points += index_penalty
            # Add penalty value to dictionary of penalties per index.
            self.penalty_per_index[index] = index_penalty

        return penalty_points

    def calc_evening_penalties(self) -> int:
        """Penalize activities in evening slots.

        Adds the penalty points to the index_penalty stored.

        Returns:
            int: The sum of all evening penalties.
        """
        penalty_points = 0
        evening_penalty = 5

        for index in self.solution:
            if self.check_index_is_empty(index) is False:
                index_info = self.translate_index(index)
                if index_info["timeslot"] == 4:
                    # Penalize for being in last timeslot.
                    penalty_points += evening_penalty
                    # Add penalty to stored dict of penalties.
                    self.penalty_per_index[index] += evening_penalty

        return penalty_points

    def calc_student_course_conflict(self, daily_schedule: list[int]) -> int:
        """Calculate the number of overlapping timeslots for a student.

        Args:
            daily_schedule (list[int]): List of timeslots at which student has activities.
        """
        return len(
            [element for element in daily_schedule if daily_schedule.count(element) > 1]
        )

    def remove_duplicates(self, schedule: list[int]) -> list[int]:
        """Ensure each conflict only counted once.

        Args:
            schedule (list[int]): List of timeslots ranging from 0 to 4."""
        return list(set(schedule))

    def calc_student_gap_penalty(
        self, daily_schedule: list[int], third_gap_penalty: int = 5
    ) -> int:
        """ "Calculate gap penalties for each student.

        Args:
            daily_schedule (list[int]): List of timeslots in a day at which student has activities.
            third_gap_penalty (int): Penalty if 3 gaps in a daily schedule. Defaults to 5.
        """
        gap_penalty_map = {0: 0, 1: 1, 2: 3, 3: third_gap_penalty}
        penalty_schedule = np.diff(np.sort(self.remove_duplicates(daily_schedule))) - 1

        return gap_penalty_map[sum(penalty_schedule)]

    def calc_student_schedule_penalties(self) -> dict[str, int]:
        """Calculate gap and conflict penalties of each schedule of each student.

        Returns:
            dict[str, int]: Key: "conflict penalties", "gap penalties".
                Value: Sum of each penalty.

        """
        total_gap_penalties = 0
        total_course_conflicts_penalties = 0

        for id in self.students:
            activities = self.get_student_schedule(id)

            student_schedule: dict[int, list[int]] = {}

            for activity in activities:
                index_info = self.translate_index(activity)
                student_schedule.setdefault(index_info["day"], []).append(
                    index_info["timeslot"]
                )

            for day in student_schedule:
                course_conflict_points = self.calc_student_course_conflict(
                    student_schedule[day]
                )
                gap_penalty_points = self.calc_student_gap_penalty(
                    student_schedule[day]
                )
                total_course_conflicts_penalties += course_conflict_points
                total_gap_penalties += gap_penalty_points

                self.penalties_per_student.update(
                    {
                        id: {
                            day: {
                                "conflict penalties": course_conflict_points,
                                "gap penalties": gap_penalty_points,
                            }
                        }
                    }
                )

        return {
            "conflict penalties": total_course_conflicts_penalties,
            "gap penalties": total_gap_penalties,
        }

    def sum_student_schedule_penalties(self) -> int:
        """Return a numeric sum of total conflict and gap penalties."""
        penalties = self.calc_student_schedule_penalties()
        return penalties["conflict penalties"] + penalties["gap penalties"]

    def modify_index_penalty(self, index: int, new_penalty: int) -> None:
        """Ädjust the stored penalty value at a given index."""
        self.penalty_per_index[index] = new_penalty

    def calc_total_penalty(self) -> int:
        """Calculate the total penalty of the schedule.

        Also updates stored value of penalty_points.

        Returns:
            int: Sum of all penalties.
        """
        total = (
            self.calc_total_capacity_penalties()
            + self.calc_evening_penalties()
            + self.sum_student_schedule_penalties()
        )

        self.penalty_points = total

        return total

    def get_penalty_at_index(self, index: int) -> int:
        """ "Returns the stored penalty at a given index."""
        return self.penalty_per_index[index]

    def sort_activities_on_enrollments(self, descending=True) -> None:
        """Sort activities on nr. of participants, from most to least participants.

        Args:
            descending (bool): Direction in which activities are to be sorted.
                Defaults to True.

        Sorting occurs inplace in self.unassgined_activities.
        """
        self.unassigned_activities = sorted(
            self.activity_enrollments,
            key=lambda key: len(self.activity_enrollments[key]),
            reverse=descending,
        )

    def calc_activity_overlap(
        self, activity1, activity2, student_overlap_value=True
    ) -> None:
        """ "Calculate the number of overlapping students or activities.

        Args:
            activity1 (tuple[str, str]): 'Course Name', 'Activity'.
            activity2 (tuple[str, str]): Same as activity1. E.G. ('Heuristieken', 'lecture 1')
        """
        overlap = len(
            self.activity_enrollments[activity1].intersection(
                self.activity_enrollments[activity2]
            )
        )
        if student_overlap_value is True:
            # Return number of overlapping students.
            return overlap
        elif overlap != 0:
            # Return overlap of activity.
            return 1
        # Return no overlap found.
        return 0

    def sort_activities_on_overlap(self, student_overlap_value=True) -> None:
        """Sort the activities in ascend of overlapping activities.

        Self.unassigned_activities is sorted in place.

        Args:
            student_overlap_value (bool): Sorts by number of overlapping students if True.
                Defaults to true. If False, only counts overlapping activities.
        """
        overlap_count = dict.fromkeys(
            (activity for activity in self.activity_enrollments), 0
        )

        for activity1 in self.activity_enrollments:
            for activity2 in self.activity_enrollments:
                if activity1[0] != activity2[0]:
                    # Ensure activities from different courses.
                    overlap_count[activity1] += self.calc_activity_overlap(
                        activity1[0], activity2[0], student_overlap_value
                    )

        self.unassigned_activities = sorted(
            overlap_count, key=lambda act: overlap_count[act], reverse=True
        )

    def shuffle_activities(self) -> None:
        """Shuffles unassigned activities in place."""
        self.unassigned_activities = random.sample(
            self.unassigned_activities, len(self.unassigned_activities)
        )

    def copy(self) -> "Model":
        """Return a copy of the model."""
        new_copy = copy.copy(self)
        new_copy.solution = copy.copy(self.solution)
        new_copy.activity_enrollments = copy.deepcopy(self.activity_enrollments)
        new_copy.unassigned_activities = [
            copy.deepcopy(tuple) for tuple in self.unassigned_activities
        ]

        return new_copy

    def check_valid_schedule_of_student(self, student: int) -> bool:
        """Evaluate if all activities of a student have been assigned to an index in the model.

        Args:
            student (int): Id index of the student.

        Returns:
            bool: True if all activities of the student have been assigned, False otherwise.
        """
        person = self.students[student]
        activities = set()
        for course in person.courses.values():
            for activity in course.activities():
                activities.add((course.name, activity.category))
        if activities == set(self.get_student_schedule(student).values()):
            return True
        print(activities, self.get_student_schedule(student))
        return False

    def is_solution(self) -> bool:
        """Evaluate if the solution is valid."""
        # Evaluate if a student with 5 courses has
        #   all activities scheduled in the solution.
        if self.check_valid_schedule_of_student(0) is False:
            return False

        # Evaluate if the number of activities is
        #   equal or greater than the standard set of activities.
        n_activities = 0
        for course in self.courses.values():
            n_activities += len(course.activities())

        activity_set = set()
        for activity in self.solution.values():
            activity_set.add(activity)

        if n_activities <= len(activity_set):
            return True
        else:
            return False

    def __repr__(self) -> str:
        return f"Model penalty points: {self.penalty_points}."

    def __add__(self, other: object) -> int:
        if isinstance(other, Model):
            return self.penalty_points + other.penalty_points
        return (
            TypeError,
            f"Addition not possible between Model and {type(other)}.",
        )

    def __sub__(self, other: object) -> int:
        if isinstance(other, Model):
            return self.penalty_points - other.penalty_points
        return (
            TypeError,
            f"Subtraction not possible between Model and {type(other)}.",
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Model):
            return self.penalty_points == other.penalty_points
        return False

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Model):
            return not self.__eq__(other)
        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Model):
            return self.penalty_points < other.penalty_points
        return False

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Model):
            return not self.__lt__(other)
        return False

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Model):
            if self.__gt__(other) or self.__eq__(other):
                return True
        return False

    def __le__(self, other: object) -> bool:
        if isinstance(other, Model):
            if self.__lt__(other) or self.__eq__(other):
                return True
            return False
