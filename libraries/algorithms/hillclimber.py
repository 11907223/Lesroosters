from libraries.algorithms.randomise import Random
import random
from typing import TYPE_CHECKING

from libraries.classes.model import Model


class HillClimber:
    """
    The HillClimber class that changes a random schedule slot in the model to a random valid value. Each improvement or
    equivalent solution is kept for the next iteration.
    """

    def __init__(self, model: Model):
        if model.is_solution() is False:
            raise Exception("Please provide a complete solution.")

        self.schedule = model.copy()
        self.penalties = model.total_penalty()

    def random_index(self, new_model: Model) -> int:
        return random.choice(list(new_model.solution))

    def swap_slots(self, new_model: Model) -> None:
        """
        Swap two slots in the schedule at random.
        """
        index_1 = self.random_index(new_model)
        index_2 = self.random_index(new_model)

        new_model.solution[index_1], new_model.solution[index_2] = (
            new_model.solution[index_2],
            new_model.solution[index_1],
        )

    def mutate_model(self, new_model: Model, number_of_slots: int = 1) -> None:
        """
        Changes the value of a number of nodes with a random valid value.
        """
        for _ in range(number_of_slots):
            self.swap_slots(new_model)

    def check_solution(self, new_model: Model) -> None:
        """
        Checks and accepts better solutions than the current solution.
        """
        new_value = new_model.total_penalty()
        old_value = self.penalties

        # We are looking for maps that cost less!
        if new_value < old_value:
            self.schedule = new_model
            self.penalties = new_value

    def run(
        self, iterations: int, verbose: bool = False, mutate_slots_number: int = 1
    ) -> None:
        """
        Runs the hillclimber algorithm for a specific amount of iterations.
        """
        self.iterations = iterations

        for iteration in range(iterations):
            # Nice trick to only print if variable is set to True
            print(
                f"Iteration {iteration}/{iterations}, current value: {self.penalties}",
                end="\r",
            ) if verbose else None

            # Create a copy of the model to simulate the change
            new_model = self.schedule.copy()

            self.mutate_model(new_model, number_of_slots=mutate_slots_number)

            # Accept it if it is better
            self.check_solution(new_model)
