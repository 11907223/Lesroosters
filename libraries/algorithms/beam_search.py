from libraries.algorithms.greedy import Greedy
from libraries.classes.model import Model
import random


class BeamSearch(Greedy):
    """Beam search algorithm that is based on the Greedy algorithm but has a beam of n.
    This algorithm creates child elements for all n states in the beam."""

    def __init__(self, empty_model: Model):
        # Use the init of the Hillclimber class
        super().__init__(empty_model)

        self.states: list = []
        self.best_solution = None
        self.best_value: float = float("inf")

    def get_next_state(self) -> Model:
        """
        Method that gets the next state from the list of states.
        """
        return self.states.pop()

    def get_empty_index(self) -> int:
        return self.model.get_empty_index()

    def get_random_activity(self, n: int) -> list(tuple):
        return random.choice(self.activity_tuples, k=n)

    def create_children(self, n: int, model: Model, index: int) -> None:
        """
        Creates the n best child-states and adds them to the list of states.
        """
        # Retrieve n random activities
        activities = self.get_random_activity(n)
        optimal_indices = []

        # Find optimal index for each activity
        for activity in activities:
            optimal_index = self.get_optimal_slot

        # Add an instance of the model to the stack, with each unique value assigned to the node.
        for value in optimal_indices:
            new_model = model.copy()
            new_model.set_value(node, value)
            self.states.append(new_model)

    def run(self, n: int) -> Model:
        """Run the beam search algorithm."""

        # Initialize list with first state
        self.states.append(self.solution.copy())

        step = 0
        while self.states:
            step += 1
            # Get state from list
            new_model = self.get_next_state()
            # Find empty index in state
            new_index = self.get_empty_index()
            # Create n best children for index
            self.create_children(n, new_model, new_index)
            # if done
            # calculate score

        return self.solution
