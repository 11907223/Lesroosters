from libraries.classes.model import Model


def print_results(algorithm: str, model: Model, runtime):
    """
    Prints results of a model generated with an algorithm.
    """

    print(
        f"THE BEST SCHEDULE FOUND WHEN USING {algorithm.upper()}:\n",
        model.solution,
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