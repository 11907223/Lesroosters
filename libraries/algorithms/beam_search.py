from libraries.classes.model import Model
import random


class BeamSearch:
    """
    A Depth First algorithm that builds a stack of models with a unique assignment of nodes for each instance.
    """

    def __init__(self, model: Model):
        self.model = model.copy()

        self.states = []

        self.best_solution = None
        self.best_value = float("inf")

    def get_next_state(self) -> Model:
        """
        Method that gets the next state from the list of states.
        """
        return self.states.pop()

    def get_possibilities(
        self, model: Model, index: int, beam: int, heuristic="random"
    ):
        possibilities = []
        if heuristic == "random":
            if len(model.activity_tuples) >= beam:
                possibilities = random.choices(model.activity_tuples, k=beam)
            else:
                possibilities = model.activity_tuples

        elif heuristic == "capacity":
            capacity = model.get_hall_capacity(index)

            for activity in model.activity_tuples:
                if model.get_activity_capacity(activity) < capacity:
                    possibilities.append(activity)

        return possibilities[:beam]

    def create_children(self, model: Model, index: int, beam: int) -> bool:
        """
        Creates all possible child-states and adds them to the list of states.
        """
        # Retrieve all valid possible activities for the index
        values = self.get_possibilities(model, index, beam, heuristic="capacity")

        if not values:
            return False

        # Add an instance of the model to the stack, with each unique value assigned to the node.
        for activity in values:
            new_model = model.copy()
            new_model.add_activity(index, activity)
            new_model.activity_tuples.remove(activity)
            self.states.append(new_model)

        return True

    def check_solution(self, new_model: Model) -> None:
        """
        Checks and accepts better solutions than the current solution.
        """
        new_value = new_model.total_penalty()
        old_value = self.best_value

        # We are looking for maps that cost less!
        if new_value <= old_value:
            self.best_solution = new_model
            self.best_value = new_value

    def run(self, beam=5, iterations=1, verbose: bool = False) -> None:
        """
        Runs the algorithm untill all possible states are visited.
        """
        for i in range(iterations):
            print("Best penalty: ", self.best_value)
            self.states.append(self.model.copy())

            step = 0
            while self.states:
                step += 1
                print(
                    f"Step {step}, with {len(self.states)} states, current value: {self.best_value}"
                ) if verbose else None

                new_model = self.get_next_state()

                # Retrieve a random empty index from the model.
                index = new_model.get_random_index(empty=True)

                if not self.create_children(new_model, index, beam):
                    # Stop if we find a solution
                    self.check_solution(new_model)
                    print(f"Iteration {i} penalty: ", new_model.total_penalty())
                    break

                # if self.best_value < 300:
                #     break

            # Update the input graph with the best result found.
            self.model = self.best_solution
