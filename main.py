import libraries.helpers.load_data as ld
from libraries.helpers.visualize import visualize
from libraries.algorithms.randomise import Random
from libraries.classes.model import Model
from libraries.helpers.print_results import print_results
from libraries.algorithms.greedy import Greedy, RandomGreedy
from libraries.algorithms.beam_search import BeamSearch
from libraries.algorithms.hillclimber import HillClimber
from libraries.algorithms.simulated_annealing import SimulatedAnnealing
from libraries.algorithms.random_restart import random_restart
import random
import time
import argparse

def main(algorithm, runs, heuristic):
    random.seed(0)
    empty_model = Model()

    # _________________________RANDOM ALGORITHM________________________________________
    if algorithm == 'random':
        random_algorithm = Random(empty_model)

        start_time = time.time()
        random_algorithm.run(runs=runs, verbose=True)
        runtime = start_time - time.time()

        print_results("random", random_algorithm.best_model, runtime)

    # ________________________BEAM SEARCH ALGORITHM____________________________________
    elif algorithm == 'beam_search':
        beam_search = BeamSearch(empty_model)
        print("STARTING BEAM SEARCH ALGORITHM \n")

        start_time = time.time()
        beam_search.run(beam=2, runs=runs, heuristic=heuristic, verbose=True)
        runtime = start_time - time.time()

        # visualize(beam_search.initial_model)

        print_results("beam search", beam_search.initial_model, runtime)

    # ______________________HILLCLIMBER ALGORITHM______________________________________
    elif algorithm == 'hillclimber':
        hillclimber = HillClimber(random_algorithm.best_model)
        print("\n STARTING HILLCLIMBER ALGORITHM")

        start_time = time.time()
        hillclimber.run(verbose=True, heuristics=['middle', 'day'])
        runtime = time.time() - start_time

        print_results('hillclimber', hillclimber.best_model, runtime)

    # ______________________SIMULATED ANNEALING________________________________________
    elif algorithm == 'simulated_annealing':
        simulated_annealing = SimulatedAnnealing(random_algorithm.best_model, temperature=10)

        random_restart(SimulatedAnnealing, heuristics=['middle', 'day'], verbose=True, iterations=200)
        start_time = time.time()
        simulated_annealing.run(iterations=100, verbose=True, heuristics=['middle', 'day'], type="exponential", alpha=0.95)
        runtime = time.time() - start_time

        print_results('simulated annealing', simulated_annealing.best_model, runtime)

    # ________________________GREEDY ALGORITHM_________________________________________
    elif algorithm == 'greedy':
        options = {"sort_size": False, "sort_overlap": False, "shuffle": False, None: False}
        options[heuristic] = True
        
        start_time = time.time()
        greedy_solution = Greedy(empty_model, sort=options["sort_size"], sort_overlap=options["sort_overlap"], shuffle=options["shuffle"]).run()
        runtime = time.time() - start_time

        print_results('greedy', greedy_solution, runtime)

    # ________________________RANDOMGREEDY ALGORITHM___________________________________
    elif algorithm == 'random_greedy':
        options = {"sort_size": False, "sort_overlap": False, "shuffle": False, None: False}
        options[heuristic] = True

        start_time = time.time()
        random_greedy = RandomGreedy(empty_model, sort=options["sort_size"], sort_overlap=options["sort_overlap"], shuffle=options["shuffle"]).run()
        runtime = time.time() - start_time

        print_results('randomgreedy', random_greedy, runtime)

    # __________________________BASELINE_______________________________________________
    elif algorithm == 'baseline':
        random.seed(0)
        with open("results/baseline.txt", "a+") as file:
            for i in range(10000):
                penalty = []
                for j in range(100):
                    random_schedule = Random(empty_model)
                    penalty.append(random_schedule.run().calc_total_penalty())
                    print(f"Current run: {i * 100 + j + 1}", end="\r")
                text = "\n".join([str(score) for score in penalty])
                file.write(f"\n{text}")

if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "run a specific algorithm")

    # adding arguments
    parser.add_argument("algorithm", help = "algorithm to run")
    parser.add_argument("--n", help = "number of runs", default=1, type=int)
    parser.add_argument("--hr", "--heuristics", help="heuristic(s) used in run")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.algorithm, args.n, args.hr)