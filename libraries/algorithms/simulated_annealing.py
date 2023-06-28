import random
import math
import sys
from typing import Optional
from libraries.algorithms.hillclimber import HillClimber
from libraries.classes.model import Model


class SimulatedAnnealing(HillClimber):
    """This class randomly swaps the indices of two activities.

    Each improvement is kept for the next iteration.
    Some solutions are accepted that result in a higher penalty score,
    depending on the current temperature.

    As most methods function in the same was as a HillClimber,
    this is a child of the HillClimber algorithm.
    """

    def __init__(self, model: Model, temperature: int | float = 3):
        """Initialise the Simulated Annealing algorithm class.

        Args:
            model (Model): A model with a filled in solution.
            temperature (int): starting temperature which accepts changes.
                Defaults to 3.

        Raises:
            Exception: Provided solution is invalid."""

        # Use the init method of the Hillclimber parent class.
        super().__init__(model)

        # Starting temperature and current temperature
        self.T0 = temperature
        self.T = temperature

    def update_temperature(self) -> None:
        """Update the temperature based on a cooling scheme.

        Temperature will approach zero as the
            number of the current iteration increases.

        Args:
            type (str): Type of cooling scheme.
                Can be linear or exponential. Defaults to linear.
            alpha (float): Degree of change for an exponential cooling scheme.
                Has to be a number below 1 and above 0.
                Has no effect on the linear cooling scheme.

        Raises:
            Exception: Given type not found or invalid.
            AssertionError: Given Alpha not within bounds.
        """
        if self.type == "linear":
            self.T = self.T - (self.T0 / self.iterations)
        elif self.type == "exponential":
            assert 0 < self.alpha < 1, "Value not within bounds."
            self.T = self.T * self.alpha
        else:
            raise Exception("Type not found or invalid.")

    def check_solution(self, new_model: Model) -> bool:
        """Check and accept better solutions than the current solution.

        Also sometimes accepts solutions that are worse, depending on the current
            temperature.

        Args:
            new_model (Model): A copy of the currently stored model with mutations.

        Returns:
            bool: True if new solution has been accepted, else False.
        """

        # Calculate the probability of accepting this new solution
        delta = new_model - self.best_model
        probability = math.exp(-delta / self.T)

        # Evaluate against a random number between 0 and 1
        #   if the new solution is accepted.
        if random.random() < probability:
            self.best_model = new_model
            return True

        # Update the temperature
        self.update_temperature()

        return False

    def run(
        self,
        runs: int = 20,
        iterations: int = 2000,
        mutate_slots_number: int = 1,
        convergence: int = sys.maxsize,
        heuristics: Optional[list[str]] = None,
        modifier: float = 1.5,
        verbose: bool = False,
        type: str = "linear",
        alpha: float = 0.99,
    ):
        self.type = type
        self.alpha = alpha
        super().run(
            iterations,
            convergence,
            mutate_slots_number,
            heuristics,
            modifier,
            verbose,
        )

        return self.best_model, self.scores

    def __repr__(self) -> str:
        return "Simulated Annealing Algorithm"
