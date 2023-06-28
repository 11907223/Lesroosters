from libraries.algorithms.hillclimber import HillClimber
from libraries.algorithms.randomise import Random
from libraries.classes.model import Model
import random
import csv
import sys
from typing import Optional


class HillClimber_Tuner(HillClimber):
    """The HillCimber Tuner class modifies the run argument to return the number of iteration at which a given convergence has occured.

    This allows for determining an average value for convergence.
    The entire class except for its run functions identically to HillClimber.
    """

    def __init__(self, valid_model: Model) -> None:
        super().__init__(valid_model)

    def run(
        self,
        iterations: int = 2000,
        convergence: int = sys.maxsize,
        mutate_slots_number: int = 1,
        heuristics: Optional[list[str]] = None,
        modifier: float = 1.2,
        verbose: bool = False,
        store_scores: bool = False,
    ) -> int:
        super().run(
            iterations,
            convergence,
            mutate_slots_number,
            heuristics,
            modifier,
            verbose,
            store_scores,
        )
        return self.iteration


def iter_tuner(
    runs: int = 20,
    convergence: int = 200,
    seed: int = 0,
    verbose: bool = False,
) -> list[int]:
    """ "Generates a number line at which iteration convergence occurs.

    Args:
        runs (int): Number of runs to determine convergence. Defaults to 20.
        convergence (int): amount of repeated results at which convergence is assumed.
            Defaults to 20.
        seed (int): Seed at which random models are generated. Defaults to 0.
    Returns:
        list[int]: A list at which iteration convergence was found."""
    random.seed(seed)
    converged_iterations: list[int] = []
    for _ in range(runs):
        model = Random(Model()).run()
        converged_iteration = HillClimber_Tuner(model).run(
            convergence=convergence, verbose=verbose
        )
        converged_iterations.append(converged_iteration)
        print(converged_iteration)

    return converged_iterations


if __name__ == "__main__":
    list_of_convergences = iter_tuner()
    print(list_of_convergences)
    with open("results/HillClimber/Iter Tuner.csv", "a+", newline="") as file:
        csv.writer(file).writerow(list_of_convergences)
