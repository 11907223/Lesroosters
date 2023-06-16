class DepthFirst:
    def __init__(self, empty_model) -> None:
        self.model = empty_model.copy()

        self.model.add_all_students()
