from libraries.classes.model import Model
from libraries.algorithms.randomise import Random

class HillClimber(Random):
    """The HillClimber class swaps two randomly selected indices.

    Each improvement is kept for the next iteration.
    Improvements are based on a decrease in penalty points.
    """

    def __init__(self, model: Model):
        """Initialise the HillClimber algorithm.

        Args:
            model (Model): A model with a filled in solution.

        Raises:
            Exception: Provided solution is invalid.
        """
        if model.is_solution() is False:
            raise Exception("Provided solution is not valid.")

        self.model = model.copy()
        self.lowest_penalty = model.total_penalty()

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
        self, iterations: int, verbose: bool = False, mutate_slots_number: int = 1
    ) -> Model:
        """Run the hillclimber algorithm for a specified number of iterations.

        Args:
            iterations (int): Number of iterations for the Hillclimber to 'climb'.
            mutate_slots_number (int): Number of mutations to occur each iteration.
            verbose (bool): Evaluate if run prints current iteration and penalty score.
        """
        self.iterations = iterations

        for iteration in range(iterations):
            print(
                f"Iteration {iteration}/{iterations}, current penalty score: {self.lowest_penalty}    ",
                end="\r",
            ) if verbose else None

            # Create a copy of the model to simulate a mutation.
            new_model = self.model.copy()

            self.mutate_model(new_model, number_of_swaps=mutate_slots_number)

            # Accept the mutation if it is an improvement.
            self.check_solution(new_model)

        return self.model