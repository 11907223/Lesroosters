import csv
from libraries.classes.model import Model

def to_csv(
    model: Model,
    runtime: float,
    run: int,
    scores: list[int],
    filename: str,
    path="./results/random_restart",
):
    """Write the results to a csv file."""
    fieldnames = [
        "run number",
        "total penalty",
        "conflict penalty",
        "gap penalty",
        "capacity penalty",
        "runtime",
        "iteration progression",
    ]

    with open(
        f"{path}/{filename}_scores.csv", "a+", newline=""
    ) as score_file:
        csv.DictWriter(score_file, fieldnames=fieldnames, extrasaction="ignore").writerow(
            (
                {
                    fieldnames[0]: run,
                    fieldnames[1]: model.penalty_points,
                    fieldnames[2]: model.calc_student_schedule_penalties()['conflict penalties'],
                    fieldnames[3]: model.calc_student_schedule_penalties()['gap penalties'],
                    fieldnames[3]: model.calc_total_capacity_penalties(),
                    fieldnames[4]: model.calc_evening_penalties(),
                    fieldnames[5]: round(runtime, 3),
                    fieldnames[6]: scores,
                }
            )
        )