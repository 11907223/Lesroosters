from libraries.classes.model import Model

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
        lowest_penalty = 1000
        for index in self.empty_slots:
            added = self.model.add_activity(index, activity_tuple)

            if added is True:
                new_penalty = self.model.total_penalty()

                # if penalty unchanged, optimal index is found
                if new_penalty == previous_penalty:
                    optimal_index = index
                    lowest_penalty = new_penalty
                    self.model.remove_activity(index=index)
                    break

                # if penalty lower than best, save index and penalty
                elif new_penalty < lowest_penalty:
                    lowest_penalty = new_penalty
                    optimal_index = index

                self.model.remove_activity(index=index)

        return optimal_index, lowest_penalty

    def run(self) -> Model:
        # loop over activities
        previous_penalty = 0
        for activity_tuple in self.activity_tuples:
            # find optimal index
            optimal_index, lowest_penalty = self.get_optimal_index(activity_tuple, previous_penalty)

            # add activity to optimal index
            self.model.add_activity(optimal_index, activity_tuple)

            # update current penalty
            previous_penalty = lowest_penalty

            # update empty slots
            self.empty_slots.remove(optimal_index)

        return self.model

    # VOOR RANDOM GREEDY
    # randomly shuffle activities
    # or make heuristic choice x % of the time, random choice x % of the time
class RandomGreedy(Greedy):
    pass