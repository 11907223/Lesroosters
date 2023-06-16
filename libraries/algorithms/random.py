from random import randrange

class Random:
    def __init__(self, empty_model):
        self.model = empty_model.copy()

        # add students to activities
        for activity_tuple in self.model.participants:
            for student in self.model.students:
                self.model.add_student(student, activity_tuple)
    
    def run(self):

        for activity_tuple in self.model.participants:
            random_slot = randrange(145)
            self.model.add_activity(random_slot, activity_tuple)
        return self.model