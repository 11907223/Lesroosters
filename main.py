import libraries.helpers.load_data as ld
from libraries.algorithms.randomise import Random
from libraries.classes.model import Model
from libraries.helpers.print_results import print_results
from libraries.algorithms.greedy import Greedy, RandomGreedy
from libraries.algorithms.beam_search import BeamSearch
from libraries.algorithms.hillclimber import HillClimber
from libraries.algorithms.simulated_annealing import SimulatedAnnealing
import random
import time
import random

if __name__ == "__main__":
    courses = ld.load_courses()
    students = ld.load_students(courses)
    halls = ld.load_halls()

    empty_model = Model()

    # _________________________RANDOM ALGORITHM________________________________________
    # random_algorithm = Random(empty_model)

    # start_time = time.time()
    # random_algorithm.run(runs=20, verbose=True)
    # runtime = start_time - time.time()

    # print_results("random", random_algorithm.model, runtime)

    # ________________________BEAM SEARCH ALGORITHM____________________________________

    beam_search = BeamSearch(empty_model)
    print("STARTING BEAM SEARCH ALGORITHM \n")

    start_time = time.time()
    beam_search.run(beam=1, runs=10, heuristic="capacity", verbose=True)
    runtime = start_time - time.time()

    print_results("beam search", beam_search.model, runtime)

    # ______________________HILLCLIMBER ALGORITHM______________________________________
    # hillclimber = HillClimber(random_algorithm.model)
    # print("\n STARTING HILLCLIMBER ALGORITHM")

    # start_time = time.time()
    # hillclimber.run(verbose=True, heuristics=['middle', 'day'])
    # runtime = time.time() - start_time

    # print_results('hillclimber', hillclimber.model, runtime)

    # ______________________SIMULATED ANNEALING________________________________________
    # simulated_annealing = SimulatedAnnealing(random_algorithm.model, temperature=10)

    # start_time = time.time()
    # simulated_annealing.run(verbose=True, heuristics=['middle', 'day'])
    # runtime = time.time() - start_time

    # print_results('simulated annealing', simulated_annealing.model, runtime)

    # ________________________GREEDY ALGORITHM_________________________________________
    # start_time = time.time()
    # greedy_solution = Greedy(empty_model).run()
    # runtime = time.time() - start_time

    # print_results('greedy', greedy_solution, runtime)

    # ________________________RANDOMGREEDY ALGORITHM___________________________________
    # start_time = time.time()
    # random_greedy = RandomGreedy(empty_model).run()
    # runtime = time.time() - start_time

    # print_results('randomgreedy', random_greedy, runtime)

    # __________________________BASELINE_______________________________________________
    random.seed(10)
    with open("baseline.txt", "a+") as file:
        for i in range(10000):
            penalty = []
            for j in range(100):
                random_schedule = Random(empty_model)
                penalty.append(random_schedule.run().calc_total_penalty())
                print(f"Current run: {i * 100 + j + 1}", end="\r")
            # print("\n".join([str(score) for score in penalty]))
            text = "\n".join([str(score) for score in penalty])
            file.write(f"\n{text}")
