from libraries.classes.model import Model
import random

class Greedy:
    """
    Greedy class constructively generates a schedule by locally taking optimal decisions.
    """
    def __init__(self, empty_model: Model, heuristic="shuffle") -> None:
        self.model = empty_model.copy()
        self.activities = list(self.model.participants.keys())
        self.empty_slots = list(self.model.solution.keys())
        if heuristic == "shuffle":
            self.shuffle_activities()

    def shuffle_activities(self):
        self.activities = random.sample(self.activities, len(self.activities))

    def get_optimal_index(self, activity: tuple[str, str], current_penalty: int):
        """
        Returns the best spot for a given activity.
        """
        # loop over timeslots
        lowest_penalty = 100000
        for index in self.empty_slots:
            added = self.model.add_activity(index, activity)

            if added is True:
                new_penalty = self.model.total_penalty()

                # if penalty unchanged, optimal index is found
                if new_penalty == current_penalty:
                    optimal_index  = index
                    lowest_penalty = new_penalty
                    self.model.remove_activity(index=index)
                    
                    return optimal_index, lowest_penalty

                # if penalty lower than best, save index and penalty
                elif new_penalty < lowest_penalty:
                    lowest_penalty = new_penalty
                    optimal_index  = index

                self.model.remove_activity(index=index)

        return optimal_index, lowest_penalty

    def run(self) -> Model:
        current_penalty = 0
        for activity in self.activities:

            # find optimal index
            optimal_index, lowest_penalty = self.get_optimal_index(activity, current_penalty)

            # add activity to optimal index
            self.model.add_activity(optimal_index, activity)

            # update current penalty
            current_penalty = lowest_penalty
            print('penalty:', current_penalty, end='\r')

            # update empty slots
            print(optimal_index)
            # print(self.empty_slots)
            self.empty_slots.remove(optimal_index)

        return self.model

class RandomGreedy(Greedy):
    """"
    Combines random and greedy choices to contructively generate a schedule.
    """
        
    def insert_randomly(self, activity: tuple[str, str]):
        """
        Inserts activity at random index.
        """
        index = self.model.get_random_index(empty=True)
        self.model.add_activity(index, activity)
        return self.model.total_penalty()
    
    def insert_greedily(self, activity: tuple[str, str], current_penalty):
        """
        Inserts activity greedily.
        """
        index, penalty = self.get_optimal_index(activity, current_penalty)
        self.model.add_activity(index, activity)
        return penalty

    def run(self, random_chance=0.2):
        current_penalty = 0
        for activity in self.activities:
            
            # make random or greedy choice
            number = random.random()
            if number < random_chance:
                penalty = self.insert_randomly(activity)
            else:
                penalty = self.insert_greedily(activity, current_penalty)
            
            # update penalty
            if penalty:
                current_penalty = penalty
            else:
                current_penalty = self.model.total_penalty()
            print('penalty:', current_penalty, end='\r')

        return self.model