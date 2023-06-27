from libraries.classes.model import Model
from libraries.algorithms.randomise import Random
import random
import heapq
import time


class BeamSearch(Random):
    """The BeamSearch algorithm implements a constructive Depth First - Beam Search algorithm.

    In this class, a state is a schedule.
    The first state is a empty schedule, the final states are filled schedules.
    Schedules and thus states, are represented by the Model class.
    Each step, n child states are created.
    Child states can be made according to several heuristics:
    Random, based on capacity or based on total penalty.

    This is a child of the Random() algorithm due to overlapping checking function and inits.
    """

    def __init__(self, model: Model):
        """Initialise the BeamSearch algorithm.

        Args:
            model (Model): An empty model.
        """
        super().__init__(model)

        self.queue: list[tuple[int, Model]] = []

    def reset_model(self) -> None:
        """Reset the model and queue of the BeamSearch class."""
        self.initial_model = Model()
        self.queue = []

    def get_next_state(self) -> Model:
        """Return the next model from the list of states."""
        state = heapq.heappop(self.queue)
        return state[1]

    def get_tot_penalty_possibilities(
        self, model: Model, index: int, n: int
    ) -> list[tuple[str, str]]:
        """Gets n possible activities that would fit in specific index of a model.
        Possibilities are selected according to the total penalty.

        Args:
            model (Model): A model for wich the possibile activities are calculated.
            index (int): The index in the model for wich possible activties are calculated.
            n (int): The beam width, how many possible activities should be returned.

        Returns:
            list[Tuple(str,str)]: A list with activity tuples of length n.
        """
        possibilities = {}

        # Check if activity capacity matches hall capacity
        for activity in model.unassigned_activities:
            model.add_activity(index, activity)
            penalty = model.calc_total_penalty()

            possibilities.update({activity: penalty})

            model.remove_activity(index=index)

        return self.sort_possibilities(n, possibilities, heuristic="totalpenalty")

    def get_capacity_possibilities(
        self, model: Model, index: int, n: int
    ) -> list[tuple[str, str]]:
        """Get n possible activities that would fit in specific index of a model.

        Possibilities are selected as possibilities according to capacity.

        Args:
            model (Model): A model for wich the possibile activities are calculated.
            index (int): The index in the model for wich possible activties are calculated.
            n (int): The beam width specifying amount of possible activities to be returned.

        Returns:
            list[Tuple(str,str)]: A list with activity tuples of length n.
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

        return self.sort_possibilities(n, possibilities, no_possibilities)

    def sort_possibilities(
        self, n: int, possibilities: dict, no_possibilities={}, heuristic="capacity"
    ) -> list[tuple[str, str]]:
        """Sort all possibilities according to heuristic and returns them.

        Args:
            n (int): The beam width, how many possible activities should be returned.
            possibilities (dict): Dictionary of possible activities mapped to their capacity.
            no_possibilities (dict): Dictionary of not possible activities mapped to their capacity.
            heuristic (str): Defaults to  'capacity', second option is "totalpenalty".

        Returns:
            list[Tuple(str,str)]: A list with activity tuples of length n.
        """

        # If there are possibilities
        if possibilities:
            if heuristic == "totalpenalty":
                # Sort possibilities in ascending order
                sorted_possibilities = sorted(possibilities.items(), key=lambda x: x[1])
            else:
                # Sort possibilities in descending order
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
        """Get n possible activities that would fit in specific index of a model.

        Possibilities are be calculated according to heuristic.

        Args:
            model (Model): A model for wich the possibile activities are calculated.
            index (int): The index in the model for wich possible activties are calculated.
            n (int): The beam width, how many possible activities should be returned.
            heuristic (str): The heurisitc that should be used to calculate possible activities.
                Options are "random", "capacity", "totalpenalty". Defaults to 'random'.

        Returns:
            list[Tuple(str,str)]: A list with activity tuples of length n.

        """

        if heuristic == "capacity":
            possibilities = self.get_capacity_possibilities(model, index, n)
            return possibilities
        elif heuristic == "totalpenalty":
            possibilities = self.get_tot_penalty_possibilities(model, index, n)
            return possibilities

        # If no heursitic was passed as argument, pick random activities
        if len(model.unassigned_activities) >= n:
            possibilities = random.choices(model.unassigned_activities, k=n)
        else:
            # If list activities smaller than n, return full list
            possibilities = model.unassigned_activities

        return possibilities

    def calc_priority(self, model: Model) -> int:
        """Calculate the priority of a model.

        The priority of a model is based on total penalty and number of
        activities that still has to be assigned.

        Args:
            model (Model): The model that needs to be calculated.

        Returns:
            priority (int): A priority score of the model.
        """
        penalty = model.calc_total_penalty()
        unassigned = len(model.unassigned_activities)

        return penalty + (unassigned * 40)

    def create_children(
        self, model: Model, index: int, beam: int, heuristic="random"
    ) -> bool:
        """Create child-states according to the beam and the heuristic.

        Created children states are added to the list of states.

        Args:
            model (Model): The model that is used to create child-states.
            index (int): The index that will be filled in the child-states.
            beam (int): The beam, number of child-states that is created.
            heuristic (str): The heursitic that is used to create child-states,
                options are "random", "capacity" and "totalpenalty"

        Returns:
            bool: True if child-states are successfully created.
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

    def write_info_to_file(
        self, model: Model, start_time, heuristic, beam, runs
    ) -> None:
        """Writes all information on a model to a txt file results/beam_search_runtime.txt.

        Args:
            model (Model): The model that should be analysed and saved to the file.
            start_time (time): The start time of the algorithm.
            heursitic (str): The heursitic that was used to create the model.
            beam (int): The beam that was used to create the model.
            runs(int): The number of runs that the algorithm did.

        """
        runtime = time.time() - start_time

        with open(f"results/beam_search_runtime.txt", "a+") as file:
            file.write(
                f"\nHeuristic: {heuristic}, Beam: {beam}, Runtime: {runtime}, Runs: {runs} \n"
                f"total penalty: {self.initial_model.calc_total_penalty()}, capacity penalty: {self.initial_model.calc_total_capacity_penalties()}, evening penalty: {self.initial_model.calc_evening_penalties()} \n"
                f"student penalty: {self.initial_model.calc_student_schedule_penalties()} \n"
                f"correct solution: {self.initial_model.is_solution()}\n"
            )

    def run(self, beam=2, runs=1, heuristic="random", verbose: bool = False) -> Model:
        """Run the beam search algorithm untill a valid solution is found.

        Args:
            beam (int): The beam that the algorithm should use.
            runs (int): The number of times that the algorithm should run.
            heursitic (str): The heuristic that the algorithm should use,
                default is "random" and options are "capacity" and "totalpenalty"
            verbose (bool): Keeps track of runs, steps and best solution found.

        Returns:
            model (Model): Best model out of all runs.
        """
        start_time = time.time()

        for i in range(runs):
            self.reset_model()
            priority = self.calc_priority(self.initial_model)
            heapq.heappush(self.queue, (priority, self.initial_model.copy()))

            step = 0
            while self.queue:
                step += 1
                print(
                    f"Run {i}/{runs}, step {step}, current penalty score: {self.best_model.penalty_points}           ",
                    end="\r",
                ) if verbose else None

                new_model = self.get_next_state()

                # Retrieve a random empty index from the model.
                if step % 3:
                    index = new_model.get_random_index(empty=True)
                else:
                    index = new_model.get_high_capacity_empty_index()

                if self.create_children(new_model, index, beam, heuristic) is False:
                    # Stop if a solution is found
                    self.check_solution(new_model)

                    # write penalty of solution to csv
                    with open(f"results/{heuristic}_beam_n={beam}.txt", "a+") as file:
                        file.write(f"{new_model.calc_total_penalty()}\n")

                    break

        # Update the input graph with the best result found.
        self.initial_model = self.best_model

        self.write_info_to_file(self.initial_model, start_time, heuristic, beam, runs)

        return self.initial_model
