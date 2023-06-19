from copy import deepcopy
from libraries.classes.model import Model
import random


class Greedy:
    """
    Greedy class constructively generates a schedule by locally taking optimal decisions.
    """

    def __init__(self, empty_model: Model) -> None:
        self.solution = deepcopy(empty_model.copy())
        self.activity_tuples = list(self.solution.participants.keys())
        # maybe randomly shuffle activities here

    # maybe slots arg, that carries the empty slots, so it doesnt loop over unused slots
    def get_optimal_index(self, activity_tuple, previous_penalty):
            # initial value
            lowest_points = 1000
            
            # loop over timeslots
            for slot in self.solution.solution:
                added = self.solution.add_activity(slot, activity_tuple)
                if added is True:

                    # if penalty unchanged, optimal index is found
                    if self.solution.total_penalty() == previous_penalty:
                        optimal_index = slot
                        self.solution.remove_activity(index=slot)
                        break

                    # if penalty lower than best, save index en best points
                    elif self.solution.total_penalty() < lowest_points:
                        lowest_points = self.solution.total_penalty()
                        optimal_index = slot

                    self.solution.remove_activity(index=slot)
                    
            return optimal_index
    
    def run(self) -> Model:

        # loop over activities
        previous_penalty = 0
        for activity_tuple in self.activity_tuples:

            # find optimal slot
            optimal_index = self.get_optimal_index(activity_tuple, previous_penalty)

            # add activity to optimal slot
            self.solution.add_activity(optimal_index, activity_tuple)

            # update current penalty
            previous_penalty = self.solution.total_penalty()

        return self.solution