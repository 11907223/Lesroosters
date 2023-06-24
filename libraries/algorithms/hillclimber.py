from libraries.classes.model import Model
from libraries.algorithms.randomise import Random
import sys
import numpy as np
from typing import Optional


class HillClimber(Random):
    """The HillClimber class swaps two randomly selected indices.

    Each improvement is kept for the next iteration.
    Improvements are based on a decrease in penalty points.

    If only a single run is performed, the algorithm is equivalent to a stochastic
        HillClimber. If multiple runs are performed,
        this is a Random-Restart stochastic HillClimber.
    """

    def __init__(self, valid_model: Model):
        """Initialise the HillClimber algorithm.

        Args:
            valid_model (Model): A model with a filled in solution.

        Raises:
            Exception: Provided solution is invalid.
        """
        if valid_model.is_solution() is False:
            raise Exception("Provided solution is not valid.")
        super().__init__(valid_model)

    def normalize_weights(self, new_model: Model) -> list[float]:
        highest_index_key = int(list(new_model.get_penalty_extremes(n=1, highest=True).keys())[0])
        lowest_index_key = int(list(new_model.get_penalty_extremes(n=1, highest=False).keys())[0])

        highest_penalty = new_model.get_penalty_at_(highest_index_key)
        lowest_penalty = new_model.get_penalty_at_(lowest_index_key)

        normalized_scores: list[float] = []
        for score in new_model.get_all_index_penalties().values():
            normalized_score = (score - lowest_penalty) / (highest_penalty - lowest_penalty)
            normalized_scores.append(normalized_score)

        return normalized_scores

    def increase_model_centre_weight(self, new_model, modifier: float=2):
        for index, score in new_model.get_all_index_penalties().items():
            if 1 <= new_model.translate_index(index)['timeslot'] <= 2:
                # Assign a higher value to the middle slots for swapping.
                new_score = (score + 1) * modifier
                # Ensure modifier also applying on slots with no penalty score.
                new_model.modify_index_penalty(index, new_score)

    def heuristic_balance(self, new_model: Model, modifier: float=2, centre_placement: bool=False) -> tuple[list[float], list[float]]:
        if centre_placement is True:
            self.increase_model_centre_weight(new_model, modifier)

        push_map = self.normalize_weights(new_model)
        pull_map: list[float] = list(1 - np.array(push_map))

        return push_map, pull_map

    def swap_slots(self, new_model: Model, push_map: Optional[list[float]]=None, pull_map: Optional[list[float]]=None) -> None:
        """Swap two slots in the model at random.

        Args:
            new_model (Model): A copy of the currently stored model with mutations.
        """
        # Select two random indices to swap.
        index_1 = new_model.get_random_index(weights=push_map)
        index_2 = new_model.get_random_index(weights=pull_map)

        new_model.swap_activities(index_1, index_2)

    def mutate_model(self, new_model: Model, number_of_swaps: int = 1, heuristics: Optional[list[str]]=None) -> None:
        """Swap a number of indices.

        Args:
            new_model (Model): A copy of the currently stored model with mutations.
            number_of_swaps (int): Amount of slots to be swapped.
            heuristics (list[str]): Optional list of heuristics to be used. Heuristics can be combined.
                Options are:
                    'balance': Use weighted swapping to trade indices with a 
                    high penalty score to an index with a lower penalty score,
                    'middle' : Use weighted swapping to trade indices with 
                        high penalty scores towards the centre of the schedule (timeslot 11 & 1),
                    'days' : Use weighted swapping to trade days containing 
                        high gap penalties with days containing high conflict hour penalties.
        """
        push_map = None
        pull_map = None
        if heuristics is not None:
                if "middle" in heuristics:
                    push_map, pull_map = self.heuristic_balance(new_model, centre_placement=True)
                elif "balance" in heuristics:
                    push_map, pull_map = self.heuristic_balance(new_model)
                if 'day' in heuristics:
                    print(new_model.get_worst_day("gap penalties"))

        for _ in range(number_of_swaps):
            self.swap_slots(new_model, push_map=push_map, pull_map=pull_map)

    def run(
        self,
        iterations: int=2000,
        mutate_slots_number: int=1,
        verbose: bool=False,
        convergence: int=sys.maxsize,
        heuristics: Optional[list[str]]=None,
    ) -> Model:
        """Run the hillclimber algorithm for a specified number of iterations.

        Args:
            iterations (int): Number of iterations for the Hillclimber to 'climb'.
                Defaults to 2000 iterations.
            runs (int): Number of runs for the HillClimber algorithm.
                Defaults to 1 run. If this value is changed, a shotgun hillclimber
                will be executed instead. 
                This generates a new random model for each new run.
            mutate_slots_number (int): Number of mutations to occur each iteration.
                Defaults to 1 mutation per iteration.
            verbose (bool): Evaluate if run prints current iteration and penalty score.
                Defaults to False.
            convergence (bool): Evaluate if iterations are based on convergence.
                If no value is given, convergence is not evaluated.
            heuristics (list[str]): Optional list of heuristics to be used. Heuristics can be combined.
                Options are:
                    'balance': Use weighted swapping to trade indices with a 
                    high penalty score to an index with a lower penalty score,
                    'middle' : Use weighted swapping to trade indices with 
                        high penalty scores towards the centre of the schedule (timeslot 11 & 1),
                    'days' : Use weighted swapping to trade days containing 
                        high gap penalties with days containing high conflict hour penalties.
        """
        iteration_count: str | int = iterations
        if convergence != sys.maxsize:
            iterations = sys.maxsize
            iteration_count = "∞"

        self.iterations = iterations

        convergence_counter = 0
        for iteration in range(iterations):
            print(
                f"Iteration {iteration}/{iteration_count}, Convergence counter: {convergence_counter}, current penalty score: {self.model.penalty_points}    ",
                end="\r",
            ) if verbose else None

            # Create a copy of the model to simulate a mutation.
            new_model = self.model.copy()

            self.mutate_model(new_model, mutate_slots_number, heuristics)

            new_model.update_penalty_points()

            if self.check_solution(new_model) is True:
                # Accept the mutation if it is an improvement.
                convergence_counter = 0
            elif convergence_counter > convergence:
                # Assume convergence has occured when solution remains the same for
                #   a given value of convergence_counter.
                break
            convergence_counter += 1

        return self.model