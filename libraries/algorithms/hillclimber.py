from libraries.classes.model import Model
from libraries.algorithms.randomise import Random
import sys
import numpy as np


class HillClimber(Random):
    """The HillClimber class swaps two randomly selected indices.

    Each improvement is kept for the next iteration.
    Improvements are based on a decrease in penalty points.

    If only a single run is performed, the algorithm is equivalent to a stochastic
        HillClimber. If multiple runs are performed,
        this is a Random-Restart stochastic HillClimber.
    """

    def __init__(self, valid_model: Model):
        """Initialise the HillClimber algorithm.

        Args:
            valid_model (Model): A model with a filled in solution.

        Raises:
            Exception: Provided solution is invalid.
        """
        if valid_model.is_solution() is False:
            raise Exception("Provided solution is not valid.")
        super().__init__(valid_model)

        self.starting_model = valid_model.copy()
        self.lowest_penalty = valid_model.total_penalty()
        self.best_score = self.lowest_penalty

    def fill_middle_slots(self, modifier: int = 1.2):
        for index, score in self.model.get_all_index_penalties().items():
            if 1 <= self.model.translate_index(index) <= 2:
                # Assign a higher value to the middle slots for swapping.
                score = (score + 1) * modifier
                # Ensure modifier also applying on slots with no penalty score.
                self.model.modify_penalty_of_(index, score)

        push_map = np.array(self.model.normalize_weights())
        pull_map = 1 - push_map

        
        

    def swap_slots(self, new_model: Model) -> None:
        """Swap two slots in the model at random.

        Args:
            new_model (Model): A copy of the currently stored model with mutations.
        """
        # Select two random indices to swap.
        index_1 = new_model.get_random_index()
        index_2 = new_model.get_random_index()

        new_model.swap_activities(index_1, index_2)

    def mutate_model(self, new_model: Model, number_of_swaps: int = 1) -> None:
        """Swap a number of indices.

        Args:
            new_model (Model): A copy of the currently stored model with mutations.
            number_of_swaps (int): Amount of slots to be swapped.
        """
        for _ in range(number_of_swaps):
            self.swap_slots(new_model)

    def run(
        self,
        runs: int = 1,
        iterations: int = 2000,
        mutate_slots_number: int = 1,
        verbose: bool = False,
        convergence: int = 0,
        heuristics: list[str]=[]
    ) -> Model:
        """Run the hillclimber algorithm for a specified number of iterations.

        Args:
            iterations (int): Number of iterations for the Hillclimber to 'climb'.
                Defaults to 2000 iterations.
            runs (int): Number of runs for the HillClimber algorithm.
                Defaults to 1 run.
            mutate_slots_number (int): Number of mutations to occur each iteration.
                Defaults to 1 mutation per iteration.
            verbose (bool): Evaluate if run prints current iteration and penalty score.
                Defaults to False.
            convergence (bool): Evaluate if iterations are based on convergence.
                Defaults to 0. On convergence value 0, iterations are used.
        """
        iterations = sys.maxsize if convergence > 0 else iterations
        self.iterations = iterations

        self.best_model = self.initial_model
        for run in range(runs):
            self.model = self.initial_model

            convergence_counter = 0
            for iteration in range(iterations):
                iter = "∞" if iterations == sys.maxsize else iterations
                print(
                    f"Run: {run}/{runs}, Iteration {iteration}/{iter}, Convergence counter: {convergence_counter}, current penalty score: {self.model.penalty_points}, best found score: {self.best_model.penalty_points}     ",
                    end="\r",
                ) if verbose else None

                # Create a copy of the model to simulate a mutation.
                new_model = self.model.copy()

                self.mutate_model(new_model, number_of_swaps=mutate_slots_number)
                new_model.update_penalty_points()
                # Accept the mutation if it is an improvement.
                if self.check_solution(new_model) is True:
                    convergence_counter = 0
                elif convergence_counter > convergence:
                    # Assume convergence has occured.
                    break
                convergence_counter += 1

            self.check_solution(self.model, self.best_model)

        return self.best_model
