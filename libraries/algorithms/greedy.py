from libraries.classes.model import Model
import random
import numpy as np
import sys


class Greedy:
    """
    Greedy class constructively generates a schedule by locally taking optimal decisions.

    Attributes:
        model (Model): MOdel (to be) filled  by algorithm.
        empty_slots (list[int]): Stores unfilled indices in schedule.
    """

    def __init__(self, empty_model: Model, shuffle=False, sort=False, sort_overlap=True) -> None:
        """
        Initializes a greedy algorithm.

        Args:
            empty_model (Model): empty model to be filled.
            shuffle (bool): to optionally shuffle activities.
            sort (bool): to optionally sort activities by size.
            sort_overlap (bool) : to optionally sort activities by amount of overlap with other activities.
        """
        self.model = empty_model.copy()
        self.empty_slots: list[int] = list(self.model.solution.keys())
        if shuffle:
            self.model.shuffle_activities()
        elif sort:
            self.model.sort_activities_on_enrollments(descending=True)
        elif sort_overlap:
            self.model.sort_activities_on_overlap()

    def get_optimal_index(self, activity: tuple[str, str], current_penalty: int) -> tuple[int, int]:
        """Find the best index for a given activity based on penalty points.

        Args:
            activity (tuple): Activity to find the optimal index for.
            current_penalty (int): Penalty points of the current model.

        Returns:
            tuple[int, int]:
                optimal_index (int): best index found.
                lowest_penalty (int): total penalty after inserting activity at optimal_index.
        """

        # loop over timeslots
        lowest_penalty = sys.maxsize
        for index in self.empty_slots:
            self.model.add_activity(index, activity)
            new_penalty = self.model.calc_total_penalty()

            # if penalty unchanged, optimal index is found
            if new_penalty == current_penalty:
                self.model.remove_activity(index=index)
                return index, current_penalty

            # if penalty lower than best, save index and penalty
            elif new_penalty < lowest_penalty:
                optimal_index = index
                lowest_penalty = new_penalty

            self.model.remove_activity(index=index)

        return optimal_index, lowest_penalty

    def insert_greedily(self, activity: tuple[str, str], current_penalty: int) -> int:
        """
        Inserts activity greedily.

        Args:
            activity (tuple): activity to be inserted.
            current_penalty (int): total penalty before insertion.

        Returns:
            (int) total penalty after insertion.
        """
        index, penalty = self.get_optimal_index(activity, current_penalty)
        self.model.add_activity(index, activity)
        self.update_empty_slots(index)
        return penalty

    def update_empty_slots(self, index) -> None:
        """
        Args:
            index (int): slot that has been filled.
        """
        self.empty_slots.remove(index)

    def run(self) -> Model:
        """
        Runs greedy algorithm once.

        Returns:
            model (Model): the generated solution.
        """
        current_penalty = 0
        for activity in self.model.unassigned_activities:
            current_penalty = self.insert_greedily(activity, current_penalty)
            print("penalty:", current_penalty, end="\r")

        return self.model


class RandomGreedy(Greedy):
    """
    Combines random and greedy choices to contructively generate a schedule.
    """

    def insert_randomly(self, activity: tuple[str, str]) -> int:
        """
        Inserts activity at random index while considering room size.

        Args:
            activity (tuple): activity to be inserted.

        Returns:
            (int) total penalty after insertion.
        """
        # index = self.model.get_random_index(empty=True)
        overflow = True
        while overflow:
            index = self.model.get_random_index(empty=True)
            overflow = self.capacity_overflow(index, activity)
        added = self.model.add_activity(index, activity)
        self.update_empty_slots(index)
        print(activity, added)
        return self.model.calc_total_penalty()

    def capacity_overflow(self, index, activity, max_difference=5) -> bool:
        """
        Checks if insertion causes an unreasonable capacity penalty.

        Args:
            index (int)         : where activity would be inserted.
            activity (tuple)    : activity to insert in room.
            max_difference (int): max difference allowed between #students in activity and room capacity.

        Returns:
            (bool): True if activity exceeds room capacity too much, False if not.
        """
        if self.model.calc_capacity_penalty_at_(index, activity) > max_difference:
            return True
        return False

    def calc_random_chance(self, i, start=0.7, alpha=0.064) -> float:
        """
        Gives the probability of a random insertion based on a exponential.

        Args:
            i (int)       : amount of activities inserted. 0 <= i <= 72.
            start (float) : random_chance at i = 0
            alpha (float) : exponential factor, decides the drop-off speed.

        Returns:
            (float): probability of a random insertion (high at the
                     beginning of the run, lower towards the end).
        """
        return start * np.exp(-alpha * i)

    def run(self) -> Model:
        """
        Runs random-greedy algorithm once.

        Args:
            random_chance (float): probability of a random insertion.

        Returns:
            model (Model): the generated solution.
        """
        current_penalty = 0
        random.seed(1)
        for i, activity in enumerate(self.model.unassigned_activities):
            # make random or greedy choice
            if random.random() < self.calc_random_chance(i):
                current_penalty = self.insert_randomly(activity)
            else:
                current_penalty = self.insert_greedily(activity, current_penalty)

            print(
                f'penalty: {current_penalty} capacity penalty: {self.model.calc_total_capacity_penalties()} gap penalty: {self.model.calc_student_schedule_penalties()["gap penalties"]}  at activity: {i}'
            )  # , end='\r')

        return self.model