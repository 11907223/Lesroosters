from libraries.helpers.experiments.hillclimber.hillclimber_tuner import (
    iter_tuner,
)
from libraries.algorithms.hillclimber import HillClimber
from libraries.algorithms.simulated_annealing import SimulatedAnnealing
from libraries.algorithms.random_restart import random_restart
import multiprocessing
import random
import csv



def heuristic_tester(algorithm, heuristic, results):
    results[" ".join(heuristic)] = random_restart(
        algorithm=algorithm,
        seed=None,
        heuristics=heuristic,
        verbose=2,
        store_runs=True,
    )


def pool_exe(target, algorithm, heuristics):
    # Source: https://stackoverflow.com/questions/10415028/how-to-get-the-return-value-of-a-function-passed-to-multiprocessing-process
    manager = multiprocessing.Manager()
    results = manager.dict()
    jobs = []

    for heuristic in heuristics:
        p = multiprocessing.Process(target=target, args=(algorithm, heuristic, results))
        jobs.append(p)
        p.start()

    for process in jobs:
        process.join()

    return results.items()


if __name__ == "__main__":
    random.seed(0)

    # list_of_convergences = iter_tuner(verbose=True)
    # print(list_of_convergences)
    # with open("results/HillClimber/Iter Tuner.csv", 'a+', newline='') as file:
    #     csv.writer(file).writerow(list_of_convergences)

    # modifiers = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
    # results: dict[int, list[int]] = {modifier:[] for modifier in modifiers}
    # for modifier in modifiers:
    #     modifier_results = random_restart(HillClimber, seed=None, modifier=modifier, store_runs=True)
    #     results[modifier] = modifier_results
    #     print(results)

    # with open("results/HillClimber/Modifier Tuner.csv", 'a+', newline='') as file:
    #     for result in results.items():
    #         csv.writer(file).writerow(result)

    # temps = [1, 5, 10, 20, 40, 80, 160]
    # results: dict[int, list[int]] = {temp:[] for temp in temps}
    # for temp in temps:
    #     temp_results = random_restart(SimulatedAnnealing, seed=None, temperature=temp, store_runs=True, verbose=1)
    #     results[temp] = temp_results
    #     print(results)

    # with open("results/HillClimber/Simulated Annealing Temp Tuner.csv", 'a+', newline='') as file:
    #     for result in results.items():
    #         csv.writer(file).writerow(result)

    heuristics = [["balance"], ["middle"], ["days"]]

    results = pool_exe(heuristic_tester, HillClimber, heuristics)

    with open(
        "results/HillClimber/Heuristics Single Comparison.csv",
        "a+",
        newline="",
    ) as file:
        for result in results:
            csv.writer(file).writerow(result)
