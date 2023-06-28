from libraries.helpers.experiments.hillclimber_tuner import (
    iter_tuner,
)
from libraries.algorithms.hillclimber import HillClimber
from libraries.algorithms.simulated_annealing import SimulatedAnnealing
from libraries.algorithms.random_restart import random_restart
import multiprocessing
import random
import csv


def heuristic_tester(
    algorithm: HillClimber | SimulatedAnnealing,
    heuristic: list[str],
    results: dict,
) -> None:
    """Wrapper function to compare heuristics.

    This function exists for easier access for multiprocessing.

    Args:
        algorithm (HillClimber | SimulatedAnnealing): Type of argument to test heuristics on.
        heuristic (list[str]): list of heuristics to use. Can be 'days', 'middle', 'balance or a combination.'
        results (dict): a dictionary created by multiprocessing.Manager().dict().
    """
    results[" ".join(heuristic)] = random_restart(
        algorithm=algorithm,
        seed=None,
        heuristics=heuristic,
        verbose=2,
        store_runs=True,
    )


def modifier_tester(
    algorithm: HillClimber | SimulatedAnnealing, modifier: int, results: dict
) -> None:
    """ "Wrapper function to compare modifiers.

    This function exists for easier access for multiprocessing.

    Args:
        algorithm (HillClimber | SimulatedAnnealing): Type of argument to test heuristics on.
        modifier (int): modifier to be applied to heuristics.
        results (dict): a dictionary created by multiprocessing.Manager().dict().
    """
    results[modifier] = random_restart(
        algorithm=algorithm,
        modifier=modifier,
        seed=None,
        heuristics=["middle", "days"],
        verbose=2,
        store_runs=True,
    )


def temp_tester(
    algorithm: SimulatedAnnealing, temperature: int, results: dict
) -> None:
    """ "Wrapper function to compare temperatures.

    This function exists for easier access for multiprocessing.
    Simulated Annealing has to be passed as an argument to maintain the same fargs
    as the other testers. This is due to the requirements for pool_exe().

    Args:
        algorithm (SimulatedAnnealing): Does not actually do anything.
        temperature (int): temperature for cooling scheme.
        results (dict): a dictionary created by multiprocessing.Manager().dict().
    """
    results[temperature] = random_restart(
        algorithm=algorithm,
        seed=None,
        temperature=temperature,
        verbose=2,
        store_runs=True,
    )


def pool_exe(target, algorithm, iterables) -> list[tuple[int, str]]:
    """Wrapper function to call multiprocessing.

    Allows for different values to be tested to be ran concurrently.
    Will use as many cores as available and able to be assigned.

    If 3 heuristics were given, 3 cores would be used.

    Source: https://stackoverflow.com/questions/10415028/how-to-get-the-return-value-of-a-function-passed-to-multiprocessing-process

    Args:
        target (function): function to be ran concurrently.
        algorithm (HillClimber | SimulatedAnnealing): Type of argument to test heuristics on.
        iterables (list[int | str]): Value which cores should concurrently process.

    """
    manager = multiprocessing.Manager()
    results = manager.dict()
    jobs = []

    for item in iterables:
        p = multiprocessing.Process(
            target=target, args=(algorithm, item, results)
        )
        jobs.append(p)
        p.start()

    for process in jobs:
        process.join()

    return results.items()


if __name__ == "__main__":
    random.seed(0)

    # Find iteration at which convergence occurs.
    list_of_convergences = iter_tuner(verbose=True)
    with open("results/random_restart_tuning/Iter Tuner.csv", "a+", newline="") as file:
        csv.writer(file).writerow(list_of_convergences)

    # Find optimal modifier for heuristics.
    modifiers = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
    results = pool_exe(modifier_tester, HillClimber, modifiers)
    with open(
        "results/random_restart_tuning/Modifier Tuner.csv", "a+", newline=""
    ) as file:
        for result in results:
            csv.writer(file).writerow(result)

    # Find optimal temperature for simulated annealing.
    temps = [2,3,4]
    results = pool_exe(temp_tester, SimulatedAnnealing, temps)
    with open(
        "results/random_restart_tuning/Simulated Annealing Temp Tuner.csv",
        "a+",
        newline="",
    ) as file:
        for result in results:
            csv.writer(file).writerow(result)

    # Find optimal combination of heuristics.
    heuristics = [["balance"], ["middle"], ["days"]]
    results = pool_exe(heuristic_tester, HillClimber, heuristics)
    with open(
        "results/random_restart_tuning/Heuristics Single Comparison.csv",
        "a+",
        newline="",
    ) as file:
        for result in results:
            csv.writer(file).writerow(result)

    # Best heuristic was 'middle'. Test recombination of middle with the others.
    heuristics_combi = [["middle", "balance"], ["middle", "days"]]
    results = pool_exe(heuristic_tester, HillClimber, heuristics_combi)
    with open(
        "results/random_restart_tuning/Heuristics Double Comparison.csv",
        "a+",
        newline="",
    ) as file:
        for result in results:
            csv.writer(file).writerow(result)
