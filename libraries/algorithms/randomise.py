from random import randrange
from libraries.classes.model import Model

class Random:
    """
    Random generates a random schedule by randomly assigning activities to slots. 
    """
    def __init__(self, empty_model: Model):
        self.model = empty_model.copy()
    
    def insert_randomly(self, activity_tuple) -> None:
        """
        Insert activity in random slot.
        """
        # while-loop ensures activity is added
        while True:
            random_slot = randrange(145)
            if self.model.add_activity(random_slot, activity_tuple) is True:
                break

        return None
    
    def run(self) -> Model: 
        """
        Generates a random solution.
        """
        # randomly assign activities to slots
        for activity_tuple in self.model.participants:
            self.insert_randomly(activity_tuple)

        # return randomly filled model object
        return self.model

def random_algorithm(iterations, empty_model: Model) -> Model:
    """
    Generates a random solution x times and return the best one.
    """
    lowest_penalty = 1000
    for _ in range(iterations):

        # generate random schedule
        r = Random(empty_model).run()

        # save best schedule 
        penalty_points = r.total_penalty()
        if penalty_points < lowest_penalty:
            best_schedule = r.copy()
            lowest_penalty = penalty_points

    return best_schedule