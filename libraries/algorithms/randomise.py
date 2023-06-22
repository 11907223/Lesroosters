from random import randrange
from libraries.classes.model import Model
from typing import Optional

class Random:
    """
    Random generates a random schedule by randomly assigning activities to slots.
    """

    def __init__(self, initial_model: Model):
        self.initial_model = initial_model.copy()
        self.model = self.initial_model
        self.lowest_penalty = 100000 # Ensure initial value always overwritten.

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

    def check_solution(self, new_model: Model, old_model: Optional[Model]=None) -> bool:
        """
        Accept better solutions than the current solution.

        Args:
            new_model (Model): The randomly generated model.
            old_model (Model): Optional old model to compare against.

        Returns:
            bool: True if new model has been accepted, else False.
        """
        new_penalty = new_model.total_penalty()
        print(new_penalty, self.lowest_penalty)
        # print(new_model, self.model.total_penalty())
        if old_model is not None:
            if new_model < old_model:
                # Save best model between runs.
                self.best_model = new_model
                self.lowest_penalty = new_penalty
                return True
        elif new_penalty < self.lowest_penalty:
            # Save best model between iterations.
            self.model = new_model
            self.lowest_penalty = new_penalty
            return True
        return False

    def run(self, runs: int=1, verbose: bool = False) -> Model:
        """Generate random schedule x times and return the best one.

        Args:
            runs (int): Number of schedules to be generated.
            verbose (bool): To display progress in terminal.

        Returns:
            Model: The best solution that has been found.
        """
        self.runs = runs

        for run in range(runs):
            print(
                f"Run {run}/{runs}, current penalty score: {self.lowest_penalty}           ", end="\r",
            ) if verbose else None

            # copy empty model
            new_model = self.initial_model.copy()

            # create random schedule
            for activity in new_model.participants:
                self.insert_randomly(activity, new_model)

            # accept if improved
            self.check_solution(new_model)

        return self.model