from libraries.classes.model import Model
import pandas as pd
from tabulate import tabulate

def print_results(algorithm_name: str, model: Model, runtime):
    """
    Prints results of a model generated with an algorithm.
    """
    model_df = model_to_df(model)
    print(
        f"THE BEST SCHEDULE FOUND WHEN USING {algorithm_name}:\n",
        tabulate(model_df, tablefmt='psql', headers='keys', showindex=False),
        "\n POINTS: ",
        model.calc_total_penalty(),
        "\n evening points:",
        model.calc_evening_penalties(),
        "\n conflict points:",
        model.calc_student_schedule_penalties(),
        "\n capacity penalty:",
        model.calc_total_capacity_penalties(),
        "\n runtime:",
        runtime,
    )

def model_to_df(model:Model):
    """Converts model object to a pandas dataframe for pretty printing."""

    # create a list of weekdays (column headers)
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # create a list of timeslots (row headers)
    timeslots = ["9-11", "11-13", "13-15", "15-17", "17-19"]

    # formatting
    list_of_dicts = []
    for i in range(len(model.solution)):
        info = model.translate_index(i)
        day  = weekdays[info['day']]
        time = timeslots[info['timeslot']]
        hall = model.halls[info['hall']].name
        activity = model.solution[i]
        students = model.activity_enrollments[activity] if activity[0] else None
        list_of_dicts.append({

            'day':day,
            'time':time,
            'hall':hall,
            'activity': f'{activity[0]} {activity[1]}' if activity[0] else '',
            '#students': len(students) if students else ''
        })

    # convert to df
    return pd.DataFrame(list_of_dicts)