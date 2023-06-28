from libraries.algorithms.randomise import Random
from libraries.classes.model import Model
from libraries.helpers.print_results import print_results
from libraries.helpers.save_greedy_run import to_csv
from libraries.helpers.score_histogram import plot_histogram
from libraries.helpers.visualize import visualize_schedule
from libraries.algorithms.greedy import Greedy, RandomGreedy
from libraries.algorithms.beam_search import BeamSearch
from libraries.algorithms.hillclimber import HillClimber
from libraries.algorithms.simulated_annealing import SimulatedAnnealing
from libraries.algorithms.random_restart import random_restart
import random
import time
import argparse


def main(algorithm, runs, heuristic, save, visualize):
    random.seed(0)
    empty_model = Model()

    algorithms = {
        "hillclimber": HillClimber,
        "simulated_annealing": SimulatedAnnealing,
        "greedy": Greedy,
        "random_greedy": RandomGreedy,
    }

    # _________________________RANDOM ALGORITHM________________________________________
    if algorithm == "random":
        random_algorithm = Random(empty_model)

        start_time = time.time()
        random_algorithm.run(runs=runs, verbose=True)
        runtime = time.time() - start_time

        print_results("random", random_algorithm.best_model, runtime)

        if visualize:
            visualize_schedule(random_algorithm.initial_model)

    # ________________________BEAM SEARCH ALGORITHM____________________________________
    elif algorithm == "beam_search":
        beam_search = BeamSearch(empty_model)
        print("STARTING BEAM SEARCH ALGORITHM \n")

        start_time = time.time()
        beam_search.run(beam=2, runs=runs, heuristic=heuristic, save=save, verbose=True)
        runtime = time.time() - start_time

        # visualize(beam_search.initial_model)

        print_results("beam search", beam_search.initial_model, runtime)

        if visualize:
            visualize_schedule(beam_search.initial_model)

    # ______________________HILLCLIMBER & SIMULATED ANNEALING___________________________
    elif algorithm in ["hillclimber", "simulated_annealing"]:
        start_time = time.time()
        best_model = random_restart(
            algorithms[algorithm], heuristics=heuristic, verbose=2, runs=runs, save=save,
        )
        runtime = time.time() - start_time

        print_results(f"{algorithm}", best_model, runtime)

        if visualize:
            visualize_schedule(best_model)

    # ________________________GREEDY & RANDOMGREEDY ALGORITHM____________________________
    elif algorithm in ["greedy", "random_greedy"]:
        # turn on heuristic
        options = {"sort_size": False, "sort_overlap": False, "shuffle": False}
        options[heuristic] = True

        # select correct algorithm
        for run_number in range(runs):
            random.seed(run_number)

            start_time = time.time()
            greedy_solution = algorithms[algorithm](
                empty_model,
                sort=options["sort_size"],
                sort_overlap=options["sort_overlap"],
                shuffle=options["shuffle"],
            ).run()
            runtime = time.time() - start_time

            if save:
                # save and display results
                to_csv(
                    greedy_solution,
                    runtime,
                    run_number,
                    heuristic,
                    filename=f"{algorithm}_{heuristic}_{runs}runs",
                )

            print_results(algorithm, greedy_solution, runtime)
        print(f"{runs} run(s) finished.")

        if save:
            print(
                f"Results have been saved to ./results/Greedy/{algorithm}_{heuristic}_{runs}runs.csv"
            )

        if visualize:
            visualize_schedule(greedy_solution)

    # __________________________BASELINE_______________________________________________
    elif algorithm == "baseline":
        # Minimum number of runs with baseline is 100.
        with open(f"results/baseline_{runs*100}runs.txt", "a+") as file:
            for i in range(runs):
                penalty = []
                for j in range(100):
                    random_schedule = Random(empty_model)
                    penalty.append(random_schedule.run().calc_total_penalty())
                    print(f"Current run cycle: {i}; {j} out of 100", end="\r")

                text = "\n".join([str(score) for score in penalty])
                file.write(f"\n{text}")

        print(f'Baseline of {runs*100} runs finished. Results saved in ./results/baseline{runs*100}runs.txt')
        
        if save:
            plot_histogram(
                data_file=f'./results/baseline_{runs*100}runs.txt', 
                output_path='./images/', 
                output_name=f'{algorithm}_{runs*100}runs_score_distribution')
            
            print(f'histogram of score distribution plotted and saved to ./images/{algorithm}_{runs}runs_score_distribution.png')

    # invalid command
    else:
        print(
            "Error: Command must be one of the following: [random, beam_search, hillclimber, simulated_annealing, greedy, random_greedy]"
        )
        return


if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="run a specific algorithm")

    # adding arguments
    parser.add_argument("algorithm", help="algorithm to run")
    parser.add_argument("-n", help="number of runs", default=1, type=int)
    parser.add_argument(
        "-hr", "--heuristics", nargs="*", help="heuristic(s) used in run"
    )
    parser.add_argument(
        "-s", "--save", action="store_true", help="saves results in files"
    )
    parser.add_argument(
        "-v", "--visualize", action="store_true", help="visualizes schedule in pop up"
    )

    # read arguments from command line
    args = parser.parse_args()

    # formatting
    if args.heuristics == []:
        args.heuristics = None
    elif args.algorithm in ["beam_search", "greedy", "random_greedy"] and args.heurstics:
        args.heuristics = args.heuristics[0]

    # run main with provided arguments
    main(args.algorithm, args.n, args.heuristics, args.save, args.visualize)