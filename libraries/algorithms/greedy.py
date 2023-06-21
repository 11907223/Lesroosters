from libraries.classes.model import Model
import random

class Greedy:
    """
    Greedy class constructively generates a schedule by locally taking optimal decisions.
    """
    def __init__(self, empty_model: Model) -> None:
        self.model = empty_model.copy()
        self.activity_tuples = list(self.model.participants.keys())
        self.empty_slots = list(self.model.solution.keys())

    def get_optimal_index(self, activity_tuple, previous_penalty):
        """
        Returns the best spot for a given activity.
        """
        # loop over timeslots
        lowest_penalty = 100000
        for index in self.empty_slots:
            added = self.model.add_activity(index, activity_tuple)

            if added is True:
                new_penalty = self.model.total_penalty()

                # if penalty unchanged, optimal index is found
                if new_penalty == previous_penalty:
                    optimal_index = index
                    lowest_penalty = new_penalty
                    self.model.remove_activity(index=index)
                    self.empty_slots.remove(optimal_index)
                    
                    return optimal_index, lowest_penalty

                # if penalty lower than best, save index and penalty
                elif new_penalty < lowest_penalty:
                    lowest_penalty = new_penalty
                    optimal_index = index

                self.model.remove_activity(index=index)

        # update empty slots
        self.empty_slots.remove(optimal_index)

        return optimal_index, lowest_penalty

    def run(self) -> Model:
        # loop over activities
        previous_penalty = 0
        for activity_tuple in self.activity_tuples:
            # find optimal index
            optimal_index, lowest_penalty = self.get_optimal_index(
                activity_tuple, previous_penalty
            )

            # add activity to optimal index
            self.model.add_activity(optimal_index, activity_tuple)

            # update current penalty
            previous_penalty = lowest_penalty
            print('penalty:', previous_penalty, end='\r')

        return self.model

class RandomGreedy(Greedy):
    """"
    Combines random and greedy choices to contructively generate a schedule.
    """
    def shuffle_activities(self):
        self.activity_tuples = random.sample(self.activity_tuples, len(self.activity_tuples))
    
    def insert_randomly(self, activity_tuple):
        """
        Inserts activity at random index.
        """
        index = self.model.get_random_index(empty=True)
        self.model.add_activity(index, activity_tuple)
        return self.model.total_penalty()
    
    def insert_greedily(self, activity_tuple, previous_penalty):
        """
        Inserts activity greedily.
        """
        index, penalty = self.get_optimal_index(activity_tuple, previous_penalty)
        self.model.add_activity(index, activity_tuple)
        return penalty

    def run(self, random_chance=0.2):
        self.shuffle_activities()
        previous_penalty = 0
        for activity_tuple in self.activity_tuples:
            
            # make random or greedy choise
            number = random.random()
            if number < random_chance:
                penalty = self.insert_randomly(activity_tuple)
            else:
                penalty = self.insert_greedily(activity_tuple, previous_penalty)
            
            # update penalty
            if penalty:
                previous_penalty = penalty
            else:
                previous_penalty = self.model.total_penalty()
            print('penalty:', previous_penalty, end='\r')

        return self.model