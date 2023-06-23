from libraries.classes.model import Model
import random

class Greedy:
    """
    Greedy class constructively generates a schedule by locally taking optimal decisions.
    """

    def __init__(self, empty_model: Model, heuristic="shuffle") -> None:
        """
        Initialize Greedy.
        
        Args:
            model (Model): empty model to be filled.
            activities (list[tuple]): activities to be inserted.
            empty_slots (list[int]): list of slots where activities may be inserted.
            heuristic (str): shuffles activities.
        """
        self.model       = empty_model.copy()
        self.activities  = list(self.model.participants.keys())
        self.empty_slots = list(self.model.solution.keys())
        if heuristic == "shuffle":
            self.shuffle_activities()

    def shuffle_activities(self):
        """
        Shuffles list of activities to be looped over.
        """
        self.activities = random.sample(self.activities, len(self.activities))

    def get_optimal_index(self, activity: tuple[str, str], current_penalty: int):
        """
        Finds the best index for a given activity based on penalty points.

        Args:
            activity (tuple): activity to find the optimal index for.
            current_penalty (int): penalty points of the current model.

        Returns:
            optimal_index (int): best index found.
            lowest_penalty (int): total penalty after inserting activity at optimal_index.
        """      

        # loop over timeslots
        lowest_penalty = 100000
        for index in self.empty_slots:

            self.model.add_activity(index, activity)
            new_penalty = self.model.total_penalty()

            # if penalty unchanged, optimal index is found
            if new_penalty == current_penalty:
                self.model.remove_activity(index=index)
                return index, current_penalty

            # if penalty lower than best, save index and penalty
            elif new_penalty < lowest_penalty:
                optimal_index  = index
                lowest_penalty = new_penalty

            self.model.remove_activity(index=index)

        return optimal_index, lowest_penalty

    def insert_greedily(self, activity: tuple[str, str], current_penalty):
        """
        Inserts activity greedily.

        Args:
            activity (tuple): activity to be inserted.
            current_penalty (int): total penalty before insertion.
        
        Returns:
            (int) total penalty after insertion.
        """
        index, penalty = self.get_optimal_index(activity, current_penalty)
        self.model.add_activity(index, activity)
        self.update_empty_slots(index)
        return penalty

    def update_empty_slots(self, index):
        """
        Args:
            index (int): slot that has been filled.
        """
        self.empty_slots.remove(index)

    def run(self) -> Model:
        current_penalty = 0
        for activity in self.activities:
            current_penalty = self.insert_greedily(activity, current_penalty)
            print('penalty:', current_penalty, end='\r')

        return self.model

class RandomGreedy(Greedy):
    """"
    Combines random and greedy choices to contructively generate a schedule.
    """
        
    def insert_randomly(self, activity: tuple[str, str]):
        """
        Inserts activity at random index.

        Args:
            activity (tuple): activity to be inserted.
        
        Returns:
            (int) total penalty after insertion.
        """
        index = self.model.get_random_index(empty=True)
        self.model.add_activity(index, activity)
        return self.model.total_penalty()
    
    def run(self, random_chance=0.2):
        """
        Runs random-greedy algorithm once.

        Args:
            random_chance (float): probability of a random insertion.

        Returns:
            model (Model): the generated solution. 
        """
        current_penalty = 0
        for activity in self.activities:
            
            # make random or greedy choice 
            if random.random() < random_chance:
                current_penalty = self.insert_randomly(activity)
            else:
                current_penalty = self.insert_greedily(activity, current_penalty)
            
            print('penalty:', current_penalty, end='\r')

        return self.model