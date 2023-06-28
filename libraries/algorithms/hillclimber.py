from libraries.classes.model import Model
from libraries.algorithms.randomise import Random
import sys
import numpy as np
import csv
import math
from typing import Optional


class HillClimber(Random):
    """The HillClimber class utilises random swaps to reduce the penalty score of a given model.

    Each improvement is kept for the next iteration.
    Improvements are based on a decrease in penalty points.
    This HillClimber is based on a stochastic HillCimber.
    By running this HillClimber with steepest=True, it becomes a steepest ascend HillCLimber.

    This is a child of the Random() algorithm due to overlapping checking function and inits.
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

    def normalization_formula(
        self,
        highest_score: float,
        lowest_score: float,
        score_to_update: float,
        steepest: bool = False,
    ) -> float:
        """
        Calculates normalised weights based on scores in the model.

        Args:
            highest_score (float): The highest score stored.
            lowest_score (float): The lowest score stored.
            score_to_update (float): The score to update.
            steepest (bool): Evaluate if only steepest points are to be swapped.

        Returns:
            float: The score to update normalized to a value between 0 and 1.
        """
        if steepest is True:
            score_to_update = math.log(score_to_update)
        return (score_to_update - lowest_score) / (highest_score - lowest_score)

    def normalize_weights(
        self, weight_map: list[float], steepest: bool = False
    ) -> np.array:
        """Normalize weights to a value between 0 and 1.

        Args:
            weight_map (np.array): A NumPy array of list[float].
                Contains weights which map to each index in the model.

        Returns:
            A NumPy array of list[float]. Each value has been normalized to a be
                between 0 and 1.
        """
        highest_penalty = max(weight_map)
        lowest_penalty = min(weight_map)

        normalized_scores: list[float] = []
        for score in weight_map:
            normalized_score = self.normalization_formula(
                highest_penalty, lowest_penalty, score, steepest
            )
            normalized_scores.append(normalized_score)

        return np.array(normalized_scores)

    def increase_centre_weight(self, new_model, modifier: float = 1.2) -> list[float]:
        """Increase centre weight of day.

        The likelihood of placing high capacity penalty activities in timeslot
        1 (11 am) or 2 (1 pm) increases based on the modifier.
        Attempts to move high penalty activities towards the centre and
            low penalty activities out of the centre.

        Args:
            new_model (Model): The model on which the weights are based.
            modifier (float): A multiplier to apply to the weights. Defaults to 2.
                2 means pushing and pulling becomes twice as likely to marked locations.

        Returns:
            np.array: A list[float] of the increased scores after modification.
        """
        new_scores: list[float] = []
        for index, score in new_model.get_index_penalty_dict().items():
            if 1 <= new_model.translate_index(index)["timeslot"] <= 2:
                # Only timeslot 1 and 2 should recieve increased weights.
                # Ensures modifier also applying on slots with no penalty score.
                new_weights = (score + 1) * modifier
                new_scores.append(new_weights)
            else:
                new_scores.append(score)

        return np.array(new_scores)

    def increase_weight_of_days(
        self, new_model: Model, day: int, modifier: float = 1.2
    ) -> np.array:
        """Increase the likelihood of pushing or pulling to a specific day.

        Args:
            new_model (Model): The model on which the weights are based.
            day (int): day with highest conflict or gap penalty score.
            modifier (float): Factor to apply to the weights. Defaults to 2.
                2 means pushing and pulling becomes twice as likely to marked locations.

        Returns:
            np.array: A list[float] of the increased scores after modification.
        """
        new_weights: list[float] = []

        for index, score in new_model.get_index_penalty_dict().items():
            if new_model.translate_index(index)["day"] == day:
                # Only increase the weights of the correct day.
                # Ensures modifier also applying on slots with no penalty score.
                new_score = (score + 1) * modifier
                new_weights.append(new_score)
            else:
                new_weights.append(score)

        return np.array(new_weights)

    def heuristic_balancing(
        self,
        new_model: Model,
        modifier: float = 1.2,
        centre_placement: bool = False,
        day_balancing: bool = False,
        steepest: bool = False,
    ) -> tuple[np.array, np.array]:
        """Balancing of index penalties based on a given number of heuristics.

        Args:
                new_model (Model): Model to be balanced.
                modifier (float): Amount of weights to be assigned. Defaults to 2.
                    This means it becomes twice as likely for a location to be pushed
                        or pulled from.
                centre_placement (bool): Whether to increase weight of centre indices.
                    Defaults to false. Attempts to move high penalty activities towards the
                    centre and low penalty activities out of the centre.
                day_balancing (bool): Whether to increase weights based on conflicts and gaps
                    in each day. Defaults to false. Attempts to move activities from high
                    conflict days to days with high gap penalties in an attempt to balance them.
                steepest (bool): Evaluate if algorithm has to only take each steepest climb.
                    Defaults to False. Will result in deterministic algorithm behaviour.

        Returns:
            tuple[list[float], list[float]]: Two lists of weights, of the length of model.
        """
        # Initiate a list based on the stored index penalty scores.
        # Is initiated as an np.array because indices of two lists may need to be summed:
        # E.G: [2, 1] + [4, 5] = [6, 6].
        new_scores: np.array = np.array(
            list(new_model.get_index_penalty_dict().values())
        )

        if centre_placement is True:
            new_scores = self.increase_centre_weight(new_model, modifier)

        if day_balancing is True:
            worst_days = new_model.get_worst_days()
            conflict_day_map = new_scores + self.increase_weight_of_days(
                new_model, worst_days["conflict day"], modifier
            )
            gap_day_map = new_scores + self.increase_weight_of_days(
                new_model, worst_days["gap day"], modifier
            )
            push_map = self.normalize_weights(conflict_day_map, steepest)
            pull_map = self.normalize_weights(gap_day_map, steepest)
            return push_map, pull_map

        # If centre and day balancing are not selected, only normalize weights.
        # A push map is a mapping of indices with high capacity penalties.
        # A pull map is the opposite. By pulling and pushing opposites, the goal is to
        # have a net positive by having a higher decrease in capacity than the increase
        # that occurs in the increase.
        push_map = self.normalize_weights(new_scores, steepest)
        pull_map = 1 - np.array(push_map)

        return push_map, pull_map

    def swap_slots(
        self,
        new_model: Model,
        push_map: Optional[np.array] = None,
        pull_map: Optional[np.array] = None,
    ) -> None:
        """Swap two slots in the model at random.

        The push_map and the pull_map respectively increase
        the weight of high and low penalty locations.

        Args:
            new_model (Model): A copy of the currently stored model with mutations.
            push_map (np.array): A list of weights for each index.
                Higher weights at an index means a greater likelihood the index is selected.
                Defaults to None. Every index will then receive the same weight.
            pull_map (np.array): A list of weights for each index.
                Higher weights at an index means a greater likelihood the index is selected.
                Defaults to None. Every index will then receive the same weight.
        """
        # Select two random indices to swap.
        index_1 = new_model.get_random_index(weights=push_map)
        index_2 = new_model.get_random_index(weights=pull_map)

        new_model.swap_activities(index_1, index_2)

    def mutate_model(
        self,
        new_model: Model,
        number_of_swaps: int = 1,
        heuristics: Optional[list[str]] = None,
        modifier: float = 1.2,
        steepest: bool = False,
    ) -> None:
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
            modifier (float): Amount of weights to be assigned. Defaults to 2.
                    This means it becomes twice as likely for a location to be pushed
                        or pulled from.
            steepest (bool): Evaluate if algorithm has to only take each steepest climb.
                    Defaults to False. Will result in deterministic algorithm behaviour.
        """
        push_map = None
        pull_map = None
        if heuristics is not None:
            if "middle" in heuristics:
                push_map, pull_map = self.heuristic_balancing(
                    new_model,
                    centre_placement=True,
                    modifier=modifier,
                    steepest=steepest,
                )
            if "day" in heuristics:
                conflict_map, gap_map = self.heuristic_balancing(
                    new_model, day_balancing=True, modifier=modifier, steepest=steepest
                )
                push_map += conflict_map
                pull_map += gap_map
            elif "balance" in heuristics:
                push_map, pull_map = self.heuristic_balancing(
                    new_model,
                    modifier=modifier,
                    steepest=steepest,
                )

        for _ in range(number_of_swaps):
            self.swap_slots(new_model, push_map=push_map, pull_map=pull_map)

    def run(
        self,
        iterations: int = 2812,
        convergence: int = sys.maxsize,
        mutate_slots_number: int = 1,
        heuristics: Optional[list[str]] = None,
        modifier: float = 1.5,
        verbose: bool = False,
        store_scores: bool = False,
    ) -> Model:
        """Run the hillclimber algorithm for a specified number of iterations.

        Args:
            iterations (int): Number of iterations for the Hillclimber to 'climb'.
                Defaults to 2812 iterations.
            convergence (bool): Evaluate if iterations are based on convergence.
                If no value is given, convergence is not evaluated.
            mutate_slots_number (int): Number of mutations to occur each iteration.
                Defaults to 1 mutation per iteration.
            heuristics (list[str]): Optional list of heuristics to be used. Heuristics can be combined.
                Options are:
                    'balance': Use weighted swapping to trade indices with a
                        penalty score to an index with a lower penalty score,
                    'middle': Use weighted swapping to trade indices with
                        high penalty scores towards the centre of the schedule (timeslot 11 & 1),
                    'days': Use weighted swapping to trade days containing
                        high gap penalties with days containing high conflict hour penalties.
                    'steepest': Evaluate if algorithm has to only take each steepest climb.
                        Will result in deterministic algorithm behaviour.
            modifier (float): Effect a heuristic has on the heat map. Defaults to a multiplier of 1.5.
            verbose (bool): Evaluate if run prints current iteration and penalty score.
                Defaults to False.
            store_scores (bool): Evaluate if scores have to be stored for plotting. Defaults to false.
                Will store scores in results/HillClimber Algorithm.csv.
        """
        iteration_count: str | int = iterations
        if convergence != sys.maxsize:
            iterations = sys.maxsize
            iteration_count = "∞"

        self.iterations = iterations

        scores: list[int] = []

        convergence_counter = 0
        for iteration in range(iterations):
            self.iteration = iteration

            print(
                f"Iteration {iteration}/{iteration_count} "
                f"Convergence counter: {convergence_counter} ",
                f"Current penalty score: {self.best_model.penalty_points}    ",
                end="\r",
            ) if verbose else None

            # Create a copy of the model to simulate a mutation.
            new_model = self.best_model.copy()

            self.mutate_model(new_model, mutate_slots_number, heuristics, modifier)

            # Update the score of the model.
            new_model.calc_total_penalty()

            if self.check_solution(new_model) is True:
                # Accept the mutation if it is an improvement.
                convergence_counter = 0
            elif convergence_counter > convergence:
                # Assume convergence has occured when solution remains the same for
                #   a given value of convergence_counter.
                break
            convergence_counter += 1

            scores.append(self.best_model.penalty_points)
            self.scores = scores
        if store_scores is True:
            with open(f"results/{self}.csv", "a+", newline="") as file:
                csv.writer(file).writerow(scores)

        return self.best_model, scores

    def __repr__(self) -> str:
        return "HillClimber Algorithm"
