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

    def get_empty_index(self, model: Model) -> int:
        return model.get_random_index(empty=True)

    def get_random_activity(self, n: int) -> list[tuple]:
        random_activities = []

        for _ in range(n):
            if not self.activity_tuples:
                break
            activity = random.choice(self.activity_tuples)
            random_activities.append(activity)
            self.activity_tuples.remove(activity)

        return random_activities

    def check_solution(self, new_model: Model) -> None:
        """
        Checks and accepts better solutions than the current solution.
        """
        new_value = new_model.total_penalty()
        old_value = self.best_value

        # See if new schedule has a lower penalty than old schedule
        if new_value <= old_value:
            self.best_solution = new_model
            self.best_value = new_value
            print(f"New best value: {self.best_value}")

    def create_children(self, n: int, model: Model, index: int) -> bool:
        """
        Creates the n best child-states and adds them to the list of states.
        """
        # Retrieve n random activities
        activities = self.get_random_activity(n)
        previous_penalty = 0

        # Find optimal index for each activity
        for activity in activities:
            optimal_index = self.get_optimal_index(activity, previous_penalty)[0]
            new_model = model.copy()
            new_model.add_activity(optimal_index, activity)
            print("ADDD ACTIVITY: ", optimal_index, activity)
            self.states.append(new_model)

        if len(activities) < n:
            return False

        return True

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
            new_index = self.get_empty_index(new_model)
            # Create n best children for index
            children = self.create_children(n, new_model, new_index)
            self.check_solution(new_model)

            # if done
            if not children:
                # calculate score
                self.check_solution(new_model)

        self.solution = self.best_solution

        return self.solution
