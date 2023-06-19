from libraries.algorithms.greedy import Greedy
from libraries.classes.model import Model


class BeamSearch(Greedy):
    """Beam search algorithm that is based on the Greedy algorithm but has a beam of n.
    This algorithm creates child elements for all n states in the beam."""

    def __init__(self, model: Model):
        # Use the init of the Hillclimber class
        super().__init__(model)

        self.states: list = []
        self.best_solution = None
        self.best_value: float = float("inf")

    def get_next_state(self) -> Model:
        """
        Method that gets the next state from the list of states.
        """
        return self.states.pop()

    def run(self, n: int) -> Model:
        """Run the beam search algorithm."""
        self.states.append(self.model.copy())
        previous_penalty = 0
        children = []

        step = 0
        while self.states:
            step += 1
            print(
                f"Step {step}, with {len(self.states)} states, current value: {self.best_value}"
            )

            new_model = self.get_next_state()

            # Retrieve an empty index
            new_index = new_model.get_empty_index()

        # loop over activities
        for activity_tuple in self.activity_tuples:
            # find optimal slot
            for i in range(n):
                optimal_index = self.get_optimal_index(activity_tuple, previous_penalty)
                children.append(optimal_index)

            # add activity to optimal slot
            self.solution.add_activity(optimal_index, activity_tuple)

            # update current penalty
            previous_penalty = self.solution.total_penalty()

        return self.solution
