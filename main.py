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

    # _________________________RANDOM ALGORITHM________________________________________
    random_algorithm = Random(empty_model)
    random_algorithm.run(runs=20, verbose=True)

    # print(
    #     "THE BEST SCHEDULE FOUND WHEN USING RANDOM:\n",
    #     # random_algorithm.model.solution,
    #     "\nTOTAL POINTS: ",
    #     random_algorithm.model.total_penalty(),
    #     "\n evening points",
    #     random_algorithm.model.evening_penalty(),
    #     "\n student penalties:",
    #     random_algorithm.model.student_schedule_penalties(),
    #     "\n capacity penalty",
    #     random_algorithm.model.total_capacity_penalties(),
    # )
    # ________________________BEAM SEARCH ALGORITHM____________________________________

    # beam_search = BeamSearch(empty_model)
    # print("STARTING BEAM SEARCH ALGORITHM \n")
    # start_time = time.time()
    # beam_search.run(beam=5, runs=100, heuristic="capacity", verbose=True)
    # end_time = time.time()

    # print(
    #     "THE BEST SCHEDULE FOUND WHEN USING RANDOM:\n",
    #     # random_algorithm.model.solution,
    #     "\nTOTAL POINTS: ",
    #     random_algorithm.model.total_penalty(),
    #     "\n evening points",
    #     random_algorithm.model.evening_penalty(),
    #     "\n student penalties:",
    #     random_algorithm.model.student_schedule_penalties(),
    #     "\n capacity penalty",
    #     random_algorithm.model.total_capacity_penalties(),
    # )

    # ______________________HILLCLIMBER ALGORITHM______________________________________
    hillclimber = HillClimber(random_algorithm.model)
    print("\n STARTING HILLCLIMBER ALGORITHM")
    start_time = time.time()
    hillclimber.run(runs=1000, verbose=True, convergence=300)
    end_time = time.time()

    # ________________________BEAM SEARCH ALGORITHM________________________

    beam_search = BeamSearch(empty_model)
    print("STARTING BEAM SEARCH ALGORITHM \n")
    start_time = time.time()
    beam_search.run(beam=2, runs=1, heuristic="capacity", verbose=True)
    end_time = time.time()

    print(
        "THE BEST SCHEDULE FOUND WHEN USING BEAMSEARCH:\n",
        # beam_search.model.solution,
        "\nTOTAL POINTS: ",
        beam_search.model.total_penalty(),
        "\n evening points",
        beam_search.model.evening_penalty(),
        "\n student points:",
        beam_search.model.sum_student_schedule_penalties(),
        "\n capacity penalty",
        beam_search.model.total_capacity_penalties(),
        "\n run time: ",
        end_time - start_time,
    )

    # # ______________________HILLCLIMBER ALGORITHM______________________________________
    # hillclimber = HillClimber(random_algorithm.model)
    # print("\n STARTING HILLCLIMBER ALGORITHM")
    # start_time = time.time()
    # hillclimber.run(iterations=2000, verbose=True)
    # end_time = time.time()

    # print(
    #     "THE BEST SCHEDULE FOUND WHEN USING HILLCLIMBER:\n",
    #     # hillclimber.model.solution,
    #     "\nTOTAL POINTS: ",
    #     hillclimber.model.total_penalty(),
    #     "\n evening points",
    #     hillclimber.model.evening_penalty(),
    #     "\n conflict points:",
    #     hillclimber.model.student_schedule_penalties(),
    #     "\n capacity penalty",
    #     hillclimber.model.total_capacity_penalties(),
    # )

    # ______________________SIMULATED ANNEALING________________________________________
    # simulated_annealing = SimulatedAnnealing(random_solution)
    # simulated_annealing.run(iterations=2000, verbose=True)

    # print(
    #     "THE BEST SCHEDULE FOUND WHEN USING SIMULATED ANNEALING:\n",
    #     simulated_annealing.model.solution,
    #     "\n POINTS: ",
    #     simulated_annealing.model.total_penalty(),
    # )

    # ________________________GREEDY ALGORITHM_________________________________________
    # start_time = time.time()
    # greedy_solution = Greedy(empty_model).run()
    # runtime = time.time() - start_time

    # print('THE BEST SCHEDULE FOUND WHEN USING GREEDY:\n', greedy_solution.solution,
    # '\n POINTS: ', greedy_solution.total_penalty(),
    # '\n evening points', greedy_solution.evening_penalty(),
    # '\n conflict points:', greedy_solution.student_schedule_penalties(),
    # '\n capacity penalty', greedy_solution.total_capacity_penalties(),
    # '\n runtime:', runtime
    # )

    # ________________________RANDOMGREEDY ALGORITHM___________________________________
    # start_time = time.time()
    # random_greedy = RandomGreedy(empty_model).run(random_chance=0.05)
    # runtime = time.time() - start_time
    # print('THE BEST SCHEDULE FOUND WHEN USING RANDOMGREEDY:\n', random_greedy.solution,
    #     '\n POINTS: ', random_greedy.total_penalty(),
    #     '\n evening points', random_greedy.evening_penalty(),
    #     '\n conflict points:', random_greedy.student_schedule_penalties(),
    #     '\n capacity penalty', random_greedy.total_capacity_penalties(),
    #     '\n runtime', runtime
    # )

    # __________________________BASELINE_______________________________________________

    # with open("baseline.txt", "a+") as file:
    #     penalty = []
    #     for i in range(10000):
    #         for j in range(100):
    #             random_schedule = Random(empty_model)
    #             penalty.append(random_schedule.run().total_penalty())
    #         print(f"Current run: {i*j+j + i + 1}")
    #         # print("\n".join([str(score) for score in penalty]))
    #         text = '\n'.join([str(score) for score in penalty])
    #         file.write(f"\n{text}")
