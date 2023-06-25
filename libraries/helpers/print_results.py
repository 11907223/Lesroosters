from libraries.classes.model import Model

def print_results(algorithm: str, model:Model, runtime):
    """
    Prints results of a model generated with an algorithm.
    """
    
    print(f'THE BEST SCHEDULE FOUND WHEN USING {algorithm.upper}:\n', model.solution,
        '\n POINTS: ', model.total_penalty(),
        '\n evening points:', model.evening_penalty(),
        '\n conflict points:', model.student_schedule_penalties(),
        '\n capacity penalty:', model.total_capacity_penalties(),
        '\n runtime:', runtime
    )