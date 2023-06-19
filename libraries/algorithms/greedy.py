from copy import deepcopy
from libraries.classes.model import Model
import random


class Greedy:
    """
    Greedy class constructively generates a schedule by locally taking optimal decisions.
    """
    def __init__(self, empty_model: Model) -> None:
        self.model = deepcopy(empty_model.copy())
        self.activity_tuples = list(self.model.participants.keys())
        self.empty_slots = list(self.model.solution.keys())

    def get_optimal_slot(self, activity_tuple, previous_penalty):
            # reset lowest penalty
            lowest_penalty = 1000
            
            # loop over timeslots
            # for slot in self.model.solution:
            for i, slot in enumerate(self.empty_slots):
                added = self.model.add_activity(slot, activity_tuple)

                if added is True:
                    new_penalty = self.model.total_penalty()

                    # if penalty unchanged, optimal slot is found
                    if new_penalty == previous_penalty:
                        optimal_slot = slot
                        rm = i
                        lowest_penalty = new_penalty
                        self.model.remove_activity(index=slot)
                        break

                    # if penalty lower than best, save slot en best points
                    elif new_penalty < lowest_penalty:
                        lowest_penalty = new_penalty
                        rm = i
                        optimal_slot = slot

                    self.model.remove_activity(index=slot)

            # remove filled slot from empty slots
            self.empty_slots.pop(rm)

            return optimal_slot, lowest_penalty
    
    def run(self) -> Model:

        # loop over activities
        previous_penalty = 0
        for activity_tuple in self.activity_tuples:

            # find optimal slot
            optimal_slot, lowest_penalty = self.get_optimal_slot(activity_tuple, previous_penalty)

            # add activity to optimal slot
            self.model.add_activity(optimal_slot, activity_tuple)

            # update current penalty
            previous_penalty = lowest_penalty

        return self.model
    

    # VOOR RANDOM GREEDY
        # randomly shuffle activities