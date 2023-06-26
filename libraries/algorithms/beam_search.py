from libraries.classes.model import Model
import random
import heapq

random.seed(0)


class BeamSearch:
    """The BeamSearch class represents a constructive Breadth Frist - Beam Search algorithm.

    In this class, a state is a schedule.
    The first state is a empty schedule, the final states are filled schedules.
    Schedules and thus states, are represented by the Model class.
    Each step, n child states are created.
    Child states can be made according to several heuristics:
    Random, based on capacity or based on total penalty.
    """

    def __init__(self, model: Model):
        """Initialise the BeamSearch algorithm.

        Args:
            model (Model): An empty model.
        """
        self.model = model.copy()

        self.queue: list[tuple[int, Model]] = []

        self.best_solution = None
        self.best_value = float("inf")

    def reset_model(self) -> None:
        """Resets the model and queue of the BeamSearch class."""
        self.model = Model()
        self.queue = []

    def get_next_state(self) -> Model:
        """Method that gets the next state from the list of states.

        Returns:
            Model.
        """
        state = heapq.heappop(self.queue)
        return state[1]

    def get_capacity_possibilities(
        self, model: Model, index: int, n: int
    ) -> list[tuple[str, str]]:
        """Gets n possible activities that would fit in specific index of a model.
        Possibilities are selected as possibilities according to capacity.

        Args:
            model (Model): A model for wich the possibile activities are calculated.
            index (int): The index in the model for wich possible activties are calculated.
            n (int): The beam width, how many possible activities should be returned.

        Returns:
            list_possibilities (list[Tuple(str,str)]): A list with activity tuples of length n.
        """
        possibilities = {}
        no_possibilities = {}
        capacity = model.get_hall_capacity(index)

        # Check if activity capacity matches hall capacity
        for activity in model.unassigned_activities:
            activity_capacity = model.get_student_count_in_activity(activity)
            if activity_capacity < capacity:
                # If so, add activity to possibilities
                possibilities.update({activity: activity_capacity})
            else:
                # If not, add activity to no possibilities
                no_possibilities.update({activity: activity_capacity})

        return self.check_possibilities(possibilities, no_possibilities, n)

    def check_possibilities(
        self, possibilities: dict, no_possibilities: dict, n: int
    ) -> list[tuple[str, str]]:
        """Checks wether there are possibilities and returns them.

        Args:
            possibilities (dict): Dictionary of possible activities mapped to their capacity.
            no_possibilities (dict): Dictionary of not possible activities mapped to their capacity.
            n (int): The beam width, how many possible activities should be returned.

        Returns:
            sorted_possibilities (list[Tuple(str,str)]): A list with activity tuples of length n.
        """

        # If there are possibilities
        if possibilities:
            # Sort possibilities in descending order and return first n elements
            sorted_possibilities = sorted(
                possibilities.items(), key=lambda x: x[1], reverse=True
            )
            list_possibilities = [item[0] for item in sorted_possibilities]
            return list_possibilities[:n]

        # Sort no possibilities in ascending order and return first n elements
        sorted_no_possibilities = sorted(no_possibilities.items(), key=lambda x: x[1])
        list_no_possibilities = [item[0] for item in sorted_no_possibilities]
        return list_no_possibilities[:n]

    def get_possibilities(
        self, model: Model, index: int, n: int, heuristic="random"
    ) -> list[tuple[str, str]]:
        """Gets n possible activities that would fit in specific index of a model.
        Possibilities are be calculated according to heuristic.

        Args:
            model (Model): A model for wich the possibile activities are calculated.
            index (int): The index in the model for wich possible activties are calculated.
            n (int): The beam width, how many possible activities should be returned.
            heuristic (str): The heurisitc that should be used to calculate possible activities.
                Options are "random", "capacity", "totalpenalty"

        Returns:
            possibilities (list[Tuple(str,str)]): A list with activity tuples of length n.

        """

        if heuristic == "capacity":
            possibilities = self.get_capacity_possibilities(model, index, n)
            return possibilities

        # If no heursitic was passed as argument, pick random activities
        if len(model.unassigned_activities) >= n:
            possibilities = random.choices(model.unassigned_activities, k=n)
        else:
            # If list activities smaller than n, return full list
            possibilities = model.unassigned_activities

        return possibilities

    def calc_priority(self, model: Model) -> int:
        """Calculates the priority of a model, based on total penalty and number of
        activities that still has to be assigned.

        Args:
            model (Model): The model that needs to be calculated.

        Returns:
            priority (int): A priority scroe for the model.
        """
        penalty = model.total_penalty()
        unassigned = len(model.unassigned_activities)

        return penalty + (unassigned * 5)

    def create_children(
        self, model: Model, index: int, beam: int, heuristic="random"
    ) -> bool:
        """
        Creates child-states according to the beam and the heursitic,
        once created child-states are added to the list of states.

        Args:
            model (Model): The model that is used to create child-states.
            index (int): The index that will be filled in the child-states.
            beam (int): The beam, number of child-states that is created.
            heuristic (str): The heursitic that is used to create child-states,
                options are "random", "capacity" and "totalpenalty"

        Returns:
            bool: True if child-states are successfully created
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
            priority = self.calc_priority(new_model)
            heapq.heappush(self.queue, (priority, new_model))

        return True

    def check_solution(self, model: Model) -> None:
        """Checks and accepts better solutions than the current solution.

        Args:
            model (Model): The model that should be checked.
        """
        new_value = model.total_penalty()
        old_value = self.best_value

        # Minimalization of penalty score
        if new_value <= old_value:
            self.best_solution = model
            self.best_value = new_value

    def run(self, beam=2, runs=1, heuristic="random", verbose: bool = False) -> Model:
        """Runs the beam search algorithm untill a valid solution is found.

        Args:
            beam (int): The beam that the algorithm should use.
            runs (int): The number of times that the algorithm should run.
            heursitic (str): The heuristic that the algorithm should use,
                default is "random" and options are "capacity" and "totalpenalty"
            verbose (bool): Keeps track of runs, steps and best solution found.

        Returns:
            model (Model): Best model out of all runs.
        """
        for i in range(runs):
            self.reset_model()
            priority = self.calc_priority(self.model)
            heapq.heappush(self.queue, (priority, self.model.copy()))

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
                    index = new_model.get_high_capacity_empty_index()
                else:
                    index = new_model.get_random_index(empty=True)

                if self.create_children(new_model, index, beam, heuristic) is False:
                    # Stop if a solution is found
                    self.check_solution(new_model)

                    # write penalty of solution to csv
                    with open("results/beam_result.txt", "a+") as file:
                        file.write(f"{new_model.calc_total_penalty()}\n")

                    break

        # Update the input graph with the best result found.
        self.model = self.best_solution

        return self.model
