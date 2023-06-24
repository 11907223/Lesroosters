from random import randrange
from libraries.classes.model import Model
from typing import Optional
import sys


class Random:
    """
    Random generates a random schedule by randomly assigning activities to slots.
    """

    def __init__(self, initial_model: Model):
        self.initial_model = initial_model.copy()
        self.model = self.initial_model

    def insert_randomly(self, activity_tuple, new_model) -> None:
        """
        Insert activity in random slot.
        """
        # while-loop ensures activity is added
        while True:
            random_slot = randrange(145)
            if new_model.add_activity(random_slot, activity_tuple) is True:
                break

        return None

    def check_solution(self, new_model: Model) -> bool:
        """
        Accept better solutions than the current solution.

        Args:
            new_model (Model): The randomly generated model.
            old_model (Model): Optional old model to compare against.

        Returns:
            bool: True if new model has been accepted, else False.
        """
        if new_model < self.model:
            # Save best model between iterations.
            self.model = new_model
            return True
        return False

    def run(self, runs: int = 1, verbose: bool = False) -> Model:
        """Generate random schedule x times and return the best one.

        Args:
            runs (int): Number of schedules to be generated.
            verbose (bool): To display progress in terminal.

        Returns:
            Model: The best solution that has been found.
        """
        self.runs = runs

        for run in range(runs):
            penalty_score = (
                "∞"
                if self.model.penalty_points == sys.maxsize
                else self.model.penalty_points
            )
            print(
                f"Run {run}/{runs}, current penalty score: {penalty_score}      ",
                end="\r",
            ) if verbose else None

            # copy empty model
            new_model = self.initial_model.copy()

            # create random schedule
            for activity in new_model.participants:
                self.insert_randomly(activity, new_model)

            new_model.update_penalty_points()

            # Accept new model if improved.
            self.check_solution(new_model)

        return self.model
