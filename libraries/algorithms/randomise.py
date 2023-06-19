from random import randrange
from copy import deepcopy
from libraries.classes.model import Model

class Random:
    """
    Random generates a random schedule by randomly assigning activities to slots. 
    """
    def __init__(self, empty_model: Model):

        # copy empty model object
        self.model = empty_model.copy()
    
    def run(self) -> Model: 
        # randomly assign activities to slots
        for activity_tuple in self.model.participants:

            # while loop ensures activity is added
            while True:
                random_slot = randrange(145)

                # addition successful
                if self.model.add_activity(random_slot, activity_tuple) is True:
                    break

        # return randomly filled model object
        return self.model

def random_algorithm(iterations, empty_model: Model) -> Model:
    """
    Generates a random schedule x times and returns the best one.
    """
    lowest_penalty = 1000
    for _ in range(iterations):

        # generate random schedule
        r = Random(empty_model).run()

        # save best schedule 
        penalty_points = r.total_penalty()
        if penalty_points < lowest_penalty:
            best_schedule = deepcopy(r)
            lowest_penalty = penalty_points

    return best_schedule


i =0 
for index in self.solution:

    if self.solution[index][0] != None:
        i += 1