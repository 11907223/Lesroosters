from libraries.classes.model import Model
import pandas as pd 

def to_csv(solution: Model, runtime, run, heuristic, filename, path='./results/Greedy/'):
    """Writes results of a run to a csv file."""
    list_of_dicts = [
        {'heuristic'      : heuristic,
        'total penalty'   : solution.calc_total_penalty(),
        'conflict penalty': solution.calc_student_schedule_penalties()['conflict penalties'],
        'gap penalty'     : solution.calc_student_schedule_penalties()['gap penalties'],
        'capacity penalty': solution.calc_total_capacity_penalties(),
        'evening penalty' : solution.calc_evening_penalties(),
        'runtime'         : runtime,
        'run_number'      : run}
    ]
    df = pd.DataFrame(list_of_dicts)
    df.to_csv(f'{path}{filename}.csv', index=False, mode='a+', header=False)