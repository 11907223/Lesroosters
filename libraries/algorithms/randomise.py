from random import randrange
from libraries.classes.model import Model


class Random:
    """
    Random generates a random schedule by randomly assigning activities to slots.
    """

    def __init__(self, empty_model: Model):
        self.empty_model = empty_model.copy()
        self.model = self.empty_model
        self.penalties = 99999999 # Ensure initial value always overwritten.

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
        """Check and accept better solutions than the current solution.

        Args:
            new_model (Model): A copy of the currently stored model with mutations.

        Returns:
            bool: True if new solution has been accepted, else False.
        """
        new_penalties = new_model.total_penalty()
        old_penalties = self.penalties

        if new_penalties < old_penalties:
            # Store better performing models.
            self.model = new_model
            self.penalties = new_penalties
            return True
        else:
            return False

    def run(self, runs: int=1, verbose: bool = False) -> Model:
        """Run the hillclimber algorithm for a specified number of iterations.

        Args:
            iterations (int): Number of iterations for the Hillclimber to 'climb'.
            mutate_slots_number (int): Number of mutations to occur each iteration.
        """
        self.runs = runs

        for run in range(runs):
            print(
                f"Run {run}/{runs}, current penalty score: {self.penalties}           ",
                end="\r",
            ) if verbose else None

            # Create a copy of the model to simulate a mutation.
            new_model = self.empty_model.copy()

            for activity in new_model.participants:
                self.insert_randomly(activity, new_model)

            # Accept the mutation if it is an improvement.
            self.check_solution(new_model)

        return self.model
