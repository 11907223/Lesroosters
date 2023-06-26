from libraries.classes.model import Model


def print_results(algorithm: object, runtime):
    """
    Prints results of a model generated with an algorithm.
    """

    print(
        f"THE BEST SCHEDULE FOUND WHEN USING {algorithm}:\n",
        algorithm.best_model.solution,
        "\n POINTS: ",
        algorithm.best_model.calc_total_penalty(),
        "\n evening points:",
        algorithm.best_model.calc_evening_penalties(),
        "\n conflict points:",
        algorithm.best_model.calc_student_schedule_penalties(),
        "\n capacity penalty:",
        algorithm.best_model.calc_total_capacity_penalties(),
        "\n runtime:",
        runtime,
    )
