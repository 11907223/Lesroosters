from libraries.helpers.experiments.hillclimber.hillclimber_tuner import iter_tuner
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

def modifier_tester(algorithm, modifier, results):
    results[modifier] = random_restart(
        algorithm=algorithm,
        seed=None,
        heuristics=['middle','days'],
        verbose=2,
        store_runs=True,
    )

def temp_tester(algorithm, temperature, results):
    results[temperature] = random_restart(
        algorithm=algorithm,
        seed=None,
        temperature=temperature,
        verbose=2,
        store_runs=True,
    )

def pool_exe(target, algorithm, iterables):
    # Source: https://stackoverflow.com/questions/10415028/how-to-get-the-return-value-of-a-function-passed-to-multiprocessing-process
    manager = multiprocessing.Manager()
    results = manager.dict()
    jobs = []

    for item in iterables:
        p = multiprocessing.Process(target=target, args=(algorithm, item, results))
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
    # results = pool_exe(modifier_tester, HillClimber, modifiers)

    # with open("results/HillClimber/Modifier Tuner.csv", 'a+', newline='') as file:
    #     for result in results:
    #         csv.writer(file).writerow(result)

    # temps = [1, 5, 10, 20, 40, 80, 160]
    # results = pool_exe(temp_tester, SimulatedAnnealing, temps)

    # with open("results/HillClimber/Simulated Annealing Temp Tuner.csv", 'a+', newline='') as file:
    #     for result in results.items():
    #         csv.writer(file).writerow(result)

    # heuristics = [["balance"], ["middle"], ["days"]]
    # results = pool_exe(heuristic_tester, SimulatedAnnealing, heuristics)

    # with open("results/HillClimber/SimulatedAnnealing Single Comparison.csv","a+",newline="",) as file:
    #     for result in results:
    #         csv.writer(file).writerow(result)

    # heuristics_combi = [["niddle", "balance"], ["middle", "days"]]
    # results = pool_exe(heuristic_tester, SimulatedAnnealing, heuristics_combi)

    # with open("results/HillClimber/SimulatedAnnealing Double Comparison.csv","a+",newline="",) as file:
    #     for result in results:
    #         csv.writer(file).writerow(result)

    random_restart(SimulatedAnnealing, runs=9999, seed=None, heuristics=['middle', 'days'], verbose=1)