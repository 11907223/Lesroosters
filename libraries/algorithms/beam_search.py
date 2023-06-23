from libraries.classes.model import Model
import random
import heapq
import uuid

random.seed(0)


class BeamSearch:
    """
    A Depth First algorithm that builds a stack of models with a unique assignment of nodes for each instance.
    """

    def __init__(self, model: Model):
        self.model = model.copy()

        self.queue = []

        self.best_solution = None
        self.best_value = float("inf")

    def reset_model(self) -> None:
        """Resets model for new iteration."""
        # Reset variables
        self.model = Model()
        self.queue = []

    def get_next_state(self) -> Model:
        """
        Method that gets the next state from the list of states.
        """

        return heapq.heappop(self.queue)

    def get_capacity_possibilities(self, model: Model, index: int, n: int):
        """Gets n (int) possible activities that would match with the given index of a model.
        Possibilities are picked according to capacity.
        """
        possibilities = {}
        no_possibilities = {}
        capacity = model.get_hall_capacity(index)

        # Check if activity capacity matches hall capacity
        for activity in model.unassigned_activities:
            activity_capacity = model.get_student_count_in_(activity)
            if activity_capacity < capacity:
                # If so, add activity to possibilities
                possibilities.update({activity_capacity: activity})
            else:
                # If not, add activity to no possibilities
                no_possibilities.update({activity_capacity: activity})

        # If there are possibilities
        if possibilities:
            # Sort possibilities in descending order and return first n elements
            sorted_possibilities = dict(sorted(possibilities.items(), reverse=True))
            list_possibilities = list(sorted_possibilities.values())
            return list_possibilities[:n]

        # Sort no possibilities in ascending order and return first n elements
        sorted_possibilities = dict(sorted(no_possibilities.items()))
        list_possibilities = list(sorted_possibilities.values())
        return list_possibilities[:n]

    def get_possibilities(
        self, model: Model, index: int, n: int, heuristic="random"
    ) -> list[tuple[str, str]]:
        """Gets n (int) possible activities that would match with the given index of a model.
        Possibilities could be picked with no heuristic (random) or according to capacity (heursitic="capacity").
        """

        if heuristic == "capacity":
            list_possibilities = self.get_capacity_possibilities(model, index, n)
            return list_possibilities

        # If no heursitic was passed as argument, pick random activities
        if len(model.unassigned_activities) >= n:
            list_possibilities = random.choices(model.unassigned_activities, k=n)
        else:
            # If list activities smaller than n, return full list
            list_possibilities = model.unassigned_activities

        return list_possibilities

    def evaluate_priority(self, model: Model) -> int:
        penalty = model.total_penalty()
        unassigned = len(model.unassigned_activities)

        return penalty + unassigned

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
            new_model.unassigned_activities.remove(activity)
            priority = self.evaluate_priority(new_model)
            unique_id = uuid.uuid4()
            heapq.heappush(self.queue, (priority, unique_id, new_model))

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

    def run(self, beam=5, runs=1, heuristic="random", verbose: bool = False) -> None:
        """
        Runs the algorithm untill all possible states are visited.
        """
        for i in range(runs):
            self.reset_model()
            self.queue.append(self.model.copy())

            step = 0
            while self.queue:
                step += 1
                print(
                    f"Run {i}/{runs}, step {step}, current penalty score: {self.best_value}           ",
                    end="\r",
                ) if verbose else None

                new_model = self.get_next_state()

                # Retrieve a random empty index from the model.
                if step % 2:
                    index = new_model.get_high_capacity_index()
                else:
                    index = new_model.get_random_index(empty=True)

                if self.create_children(new_model, index, beam, heuristic) is False:
                    # Stop if we find a solution
                    self.check_solution(new_model)
                    # print(f"Iteration {i} penalty: ", new_model.total_penalty())

                    # write penalty of solution to csv
                    with open("results/beam_result.txt", "a+") as file:
                        file.write(f"{new_model.total_penalty()}\n")

                    break

            # print("Best penalty: ", self.best_value)

        # Update the input graph with the best result found.
        self.model = self.best_solution

        return self.model
