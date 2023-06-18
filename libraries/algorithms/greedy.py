from copy import deepcopy 
# from libraries.classes.model import Model

class Greedy:
    """
    Greedy class constructively generates a schedule by locally taking optimal decisions.
    """
    def __init__(self, empty_model) -> None:
        self.solution = deepcopy(empty_model)
    
    def run(self):
        return None