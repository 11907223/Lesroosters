from copy import deepcopy 
from libraries.classes.model import Model
import random 

class Greedy:
    """
    Greedy class constructively generates a schedule by locally taking optimal decisions.
    """
    def __init__(self, empty_model: Model) -> None:
        self.solution = deepcopy(empty_model.copy())
        self.solution.add_all_students()
        self.activity_tuples = list(self.solution.participants.keys())
        # maybe randomly shuffle activities here

    def run(self) -> Model:
        # insert first activity randomly
        self.solution.add_activity(random.randrange(145), self.activity_tuples[0])
        self.activity_tuples.pop(0)

        # loop over activities
        for activity_tuple in self.activity_tuples:

            # initial value
            lowest_points = 1000

            # loop over timeslots
            for slot in self.solution.model:

                added = self.solution.add_activity(slot, activity_tuple)
                if added is True:

                    # schedule not full enough yet
                    if self.solution.total_penalty() <= 3:
                        optimal_index = slot
                        self.solution.remove_activity(index=slot)
                        break

                    # if penalty points lower than best, save index en best points
                    elif self.solution.total_penalty() < lowest_points:
                        lowest_points = self.solution.total_penalty()
                        optimal_index = slot
                    
                    self.solution.remove_activity(index=slot)
            
            # add activity to optimal slot
            self.solution.add_activity(optimal_index, activity_tuple)

        return self.solution