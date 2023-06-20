from libraries.classes.model import Model


class HillClimber:
    """The HillClimber class swaps two randomly selected indices.

    Each improvement is kept for the next iteration.
    Improvements are based on a decrease in penalty points.
    """

    def __init__(self, model: Model):
        if model.is_solution() is False:
            raise Exception("Please provide a complete solution.")

        self.model = model.copy()
        self.penalties = model.total_penalty()

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
            number_of_slots (int): Amount of slots to be swapped.
        """
        for _ in range(number_of_swaps):
            self.swap_slots(new_model)

    def check_solution(self, new_model: Model) -> None:
        """Check and accept better solutions than the current solution.

        Args:
            new_model (Model): A copy of the currently stored model with mutations.
        """
        new_penalties = new_model.total_penalty()
        old_penalties = self.penalties

        # We are looking for maps that cost less!
        if new_penalties < old_penalties:
            self.model = new_model
            self.penalties = new_penalties

    def run(
        self, iterations: int, verbose: bool = False, mutate_slots_number: int = 1
    ) -> None:
        """Run the hillclimber algorithm for a specified number of iterations.

        Args:
            iterations (int): Number of iterations for the Hillclimber to 'climb'.
            mutate_slots_number (int): Number of mutations to occur each iteration.
        """
        self.iterations = iterations

        for iteration in range(iterations):
            print(
                f"Iteration {iteration}/{iterations}, current value: {self.penalties}",
                end="\r",
            ) if verbose else None

            # Create a copy of the model to simulate the change
            new_model = self.model.copy()

            self.mutate_model(new_model, number_of_slots=mutate_slots_number)

            # Accept it if it is better
            self.check_solution(new_model)
