from libraries.classes.model import Model

class DepthFirst:
    def __init__(self, model: Model) -> None:
        self.model = model.copy()

    def run(self, n: int, heuristic_function: function) -
