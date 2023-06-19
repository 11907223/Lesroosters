from libraries.algorithms.greedy import Greedy
from libraries.classes.model import Model


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
        return self.solution.get_empty_index()

    def build_children(self, solution: Model, index) -> None:
        """
        Creates all possible child-states and adds them to the list of states.
        """
        # Retrieve all valid possible values for the node.
        values = model.get_possibilities(node)

        # Add an instance of the model to the stack, with each unique value assigned to the node.
        for value in values:
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
            # if done
            # calculate score

        return self.solution
