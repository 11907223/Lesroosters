from random import randrange
from copy import deepcopy
from libraries.classes.model import Model

class Random:
    """
    Random class randomly assigns all activities to schedule slots. 
    """
    def __init__(self, empty_model: Model):

        # copy empty model object
        self.model = deepcopy(empty_model.copy())

        # add students to activities
        for activity_tuple in self.model.participants:
            for student in self.model.students:
                self.model.add_student(int(student), activity_tuple)
    
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