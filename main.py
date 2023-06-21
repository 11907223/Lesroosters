import libraries.helpers.load_data as ld
from libraries.algorithms.randomise import Random
from libraries.classes.model import Model
from libraries.algorithms.greedy import Greedy, RandomGreedy
from libraries.algorithms.beam_search import BeamSearch
from libraries.algorithms.hillclimber import HillClimber
from libraries.algorithms.simulated_annealing import SimulatedAnnealing
import time

if __name__ == "__main__":
    courses = ld.load_courses()
    students = ld.load_students(courses)
    halls = ld.load_halls()

    empty_model = Model()
    # print(s.get_highest_students(3))

    # start_time = time.time()

    # print("empty index: ", random_model.get_random_index())

    # _________________________RANDOM ALGORITHM_______________________
    random_algorithm = Random(empty_model)
    print("STARTING RANDOM ALGORITHM \n")
    start_time = time.time()
    random_model = random_algorithm.run(runs=1000, verbose=True)
    end_time = time.time()

    print(
        "THE BEST SCHEDULE FOUND WHEN USING RANDOM:\n",
        # random_algorithm.model.solution,
        "\nTOTAL POINTS: ",
        random_model.total_penalty(),
        "\n evening points",
        random_model.evening_penalty(),
        "\n conflict points:",
        random_model.conflict_penalty(),
        "\n capacity penalty: ",
        random_model.total_capacity_penalties(),
        "\n run time: ",
        end_time - start_time,
    )

    # ________________________BEAM SEARCH ALGORITHM________________________

    beam_search = BeamSearch(empty_model)
    print("STARTING BEAM SEARCH ALGORITHM \n")
    start_time = time.time()
    beam_search.run(beam=5, runs=100, heuristic="capacity", verbose=True)
    end_time = time.time()

    print(
        "THE BEST SCHEDULE FOUND WHEN USING BEAMSEARCH:\n",
        # beam_search.model.solution,
        "\nTOTAL POINTS: ",
        beam_search.model.total_penalty(),
        "\n evening points",
        beam_search.model.evening_penalty(),
        "\n conflict points:",
        beam_search.model.conflict_penalty(),
        "\n capacity penalty",
        beam_search.model.total_capacity_penalties(),
        "\n run time: ",
        end_time - start_time,
    )

    # ______________________HILLCLIMBER ALGORITHM_____________________
    hillclimber = HillClimber(random_algorithm.model)
    print("STARTING HILLCLIMBER ALGORITHM \n")
    start_time = time.time()
    hillclimber.run(iterations=2000, verbose=True)
    end_time = time.time()

    print(
        "THE BEST SCHEDULE FOUND WHEN USING HILLCLIMBER:\n",
        # hillclimber.model.solution,
        "\nTOTAL POINTS: ",
        hillclimber.model.total_penalty(),
        "\n evening points",
        hillclimber.model.evening_penalty(),
        "\n conflict points:",
        hillclimber.model.conflict_penalty(),
        "\n capacity penalty",
        hillclimber.model.total_capacity_penalties(),
        "\n run time: ",
        end_time - start_time,
    )

    # ______________________SIMULATED ANNEALING_____________________
    # simulated_annealing = SimulatedAnnealing(random_solution)
    # simulated_annealing.run(iterations=2000, verbose=True)

    # print(
    #     "THE BEST SCHEDULE FOUND WHEN USING SIMULATED ANNEALING:\n",
    #     simulated_annealing.model.solution,
    #     "\n POINTS: ",
    #     simulated_annealing.model.total_penalty(),
    # )

    # ________________________GREEDY ALGORITHM________________________
    # greedy_solution = Greedy(empty_model).run()
    # print('THE BEST SCHEDULE FOUND WHEN USING GREEDY:\n', greedy_solution.solution, 
    # '\n POINTS: ', greedy_solution.total_penalty(),
    # '\n evening points', greedy_solution.evening_penalty(),
    # '\n conflict points:', greedy_solution.conflict_penalty(),
    # '\n capacity penalty', greedy_solution.total_capacity_penalties() 
    # )

    # ________________________RANDOMGREEDY ALGORITHM__________________
    # random_greedy = RandomGreedy(empty_model).run(random_chance=0)
    # print('THE BEST SCHEDULE FOUND WHEN USING RANDOMGREEDY:\n', random_greedy.solution, 
    #     '\n POINTS: ', random_greedy.total_penalty(),
    #     '\n evening points', random_greedy.evening_penalty(),
    #     '\n conflict points:', random_greedy.conflict_penalty(),
    #     '\n capacity penalty', random_greedy.total_capacity_penalties() 
    # )

    # __________________________BASELINE______________________________________

    # with open("baseline.txt", "a+") as file:
    #     for _ in range(100000):
    #         random_schedule = Random(schedule, courses)
    #         random_schedule = random_schedule.run()
    #         penalty = Penalty(random_schedule)
    #         file.write(f"{penalty.total()}\n")

    # total_runtime = time.time() - start_time

    # print(time.strftime("%H:%M:%S", time.gmtime(total_runtime)))
