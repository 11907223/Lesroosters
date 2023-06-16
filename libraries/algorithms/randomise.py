from random import randrange
from copy import deepcopy

class Random:
    def __init__(self, empty_model):
        self.model = deepcopy(empty_model.copy())

        # add students to activities
        for activity_tuple in self.model.participants:
            for student in self.model.students:
                self.model.add_student(student, activity_tuple)
    
    def run(self):
        # insert activities in random slot
        for activity_tuple in self.model.participants:
            while True:
                random_slot = randrange(145)
                if not self.model.add_activity(random_slot, activity_tuple):
                    break
            
        return self.model