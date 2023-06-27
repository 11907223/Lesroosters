from libraries.algorithms.hillclimber import HillClimber
from libraries.algorithms.randomise import Random
from libraries.classes.model import Model
import random
import csv
import sys
from typing import Optional


class HillClimber_Tuner(HillClimber):
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
    random.seed(seed)
    converged_iterations: list[int] = []
    for _ in range(runs):
        model = Random(Model()).run()
        converged_iteration = HillClimber_Tuner(model).run(convergence=convergence, verbose=verbose)
        converged_iterations.append(converged_iteration)
        print(converged_iteration)

    return converged_iterations

if __name__ == "__main__":
    list_of_convergences = iter_tuner()
    print(list_of_convergences)
    with open("results/HillClimber/Iter Tuner.csv", "a+", newline="") as file:
        csv.writer(file).writerow(list_of_convergences)
