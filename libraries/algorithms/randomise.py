from random import randrange
from libraries.classes.model import Model
import sys


class Random:
    """The Random algorithm generates a schedule through random assignment of activities to indices in the schedule.

    Attributes:
        self.initial_model (Model): An empty Model object to fill in.
            Storing this allows the algorithm to generate multiple random schedules.
        self.model (Model): The best model found after running the algorithm.
    """

    def __init__(self, initial_model: Model):
        """ "Init creates a copy of the initial model to ensure pointers map to new locations."""
        self.initial_model = initial_model.copy()
        self.best_model = self.initial_model

    def insert_randomly(self, activity_tuple, new_model) -> None:
        """Insert activity in random slot."""
        # while-loop ensures activity is added
        while True:
            random_slot = randrange(145)
            if new_model.add_activity(random_slot, activity_tuple) is True:
                break

    def check_solution(self, new_model: Model) -> bool:
        """Accept better solutions than the current solution.

        Args:
            new_model (Model): The newly generated model.

        Returns:
            bool: True if new model has a lower score than the stored model, else False.
        """
        if new_model < self.best_model:
            # Save best model between iterations.
            self.best_model = new_model
            return True
        return False

    def run(self, runs: int = 1, verbose: bool = False) -> Model:
        """Generate random schedule x times and return the one with the lowest penalty score.

        Args:
            runs (int): Number of runs to be performed in search of a better schedule.
                Defaults to 1.
            verbose (bool): Evaluate if progress has to be displayed in the terminal.
                Defaults to false.

        Returns:
            Model: The model with the lowest penalty score.
        """
        self.runs = runs

        for run in range(runs):
            penalty_score = (
                "∞"
                if self.best_model.penalty_points == sys.maxsize
                else self.best_model.penalty_points
            )
            print(
                f"Run {run}/{runs}, current penalty score: {penalty_score}      ",
                end="\r",
            ) if verbose else None

            # Copy empty model.
            new_model = self.initial_model.copy()

            # Create random schedule.
            for activity in new_model.activity_enrollments:
                self.insert_randomly(activity, new_model)

            # Update penalty points of new model.
            new_model.calc_total_penalty()

            # Accept new model if improved.
            self.check_solution(new_model)

        return self.best_model

    def __repr__(self) -> str:
        return "Random Algorithm"
