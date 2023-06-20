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
        self, model: Model, index: int, n: int, heuristic="random"
    ) -> list[tuple[str, str]]:
        """Gets n (int) possible activities that would match with the given index of a model.
        Possibilities could be picked with no heuristic (random) or according to capacity (heursitic="capacity").
        """
        possibilities = []

        if heuristic == "random":
            if len(model.activity_tuples) >= n:
                # Pick random activities
                possibilities = random.choices(model.activity_tuples, k=n)
            else:
                # If list activities smaller than n, return full list
                possibilities = model.activity_tuples

        elif heuristic == "capacity":
            capacity = model.get_hall_capacity(index)

            # Check if activity capacity matches hall capacity
            for activity in model.activity_tuples:
                if model.get_activity_capacity(activity) < capacity:
                    possibilities.append(activity)

        return possibilities[:n]

    def create_children(
        self, model: Model, index: int, beam: int, heuristic="random"
    ) -> bool:
        """
        Creates all possible child-states and adds them to the list of states.
        """
        # Retrieve all valid possible activities for the index
        values = self.get_possibilities(model, index, beam, heuristic)

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

        # Minimalization of penalty score
        if new_value <= old_value:
            self.best_solution = new_model
            self.best_value = new_value

    def run(
        self, beam=5, iterations=1, heuristic="random", verbose: bool = False
    ) -> None:
        """
        Runs the algorithm untill all possible states are visited.
        """
        for i in range(iterations):
            # Reset variables
            self.model = Model()
            self.states = []
            self.model.activity_tuples = list(self.model.participants.keys())
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

                if not self.create_children(new_model, index, beam, heuristic):
                    # Stop if we find a solution
                    self.check_solution(new_model)
                    print(f"Iteration {i} penalty: ", new_model.total_penalty())
                    break

                # if self.best_value < 300:
                #     break

            print("Best penalty: ", self.best_value)

        # Update the input graph with the best result found.
        self.model = self.best_solution
