import libraries.helpers.load_data as ld
from libraries.algorithms.randomise import Random, random_algorithm
from libraries.classes.model import Model
from libraries.algorithms.greedy import Greedy
from libraries.algorithms.hillclimber import HillClimber
from libraries.algorithms.simulated_annealing import SimulatedAnnealing

if __name__ == "__main__":
    courses = ld.load_courses()
    students = ld.load_students(courses)
    halls = ld.load_halls()

    empty_model = Model()
    random_model = Random(empty_model).run()
    # print(s.get_highest_students(3))

    # start_time = time.time()

    print("empty index: ", random_model.get_empty_index())

    # _________________________RANDOM ALGORITHM_______________________
    iterations = 1
    random_solution = random_algorithm(iterations, empty_model)

    print(
        "THE BEST SCHEDULE FOUND WHEN USING RANDOM:\n",
        random_solution.solution,
        "\nPOINTS: ",
        random_solution.total_penalty(),
    )
    # ________________________________________________________________

    # ______________________HILLCLIMBER ALGORITHM_____________________
    hillclimber = HillClimber(random_solution)
    hillclimber.run(iterations=2000, verbose=True)

    print(
        "THE BEST SCHEDULE FOUND WHEN USING HILLCLIMBER:\n",
        hillclimber.schedule.solution,
        "\nPOINTS: ",
        hillclimber.schedule.total_penalty(),
    )

    # ______________________SIMULATED ANNEALING_____________________
    simulated_annealing = SimulatedAnnealing(random_solution)
    simulated_annealing.run(iterations=2000, verbose=True)

    print(
        "THE BEST SCHEDULE FOUND WHEN USING SIMULATED ANNEALING:\n",
        simulated_annealing.schedule.solution,
        "\n POINTS: ",
        simulated_annealing.schedule.total_penalty(),
    )

    # ________________________GREEDY ALGORITHM________________________
    # greedy_solution = Greedy(empty_model).run()
    # print('THE BEST SCHEDULE FOUND WHEN USING GREEDY:\n', greedy_solution.solution, '\n POINTS: ', greedy_solution.total_penalty())
    # __________________________BASELINE______________________________________

    # with open("baseline.txt", "a+") as file:
    #     for _i in range(100000):
    #         random_schedule = Random(schedule, courses)
    #         random_schedule = random_schedule.run()
    #         penalty = Penalty(random_schedule)
    #         file.write(f"{penalty.total()}\n")

    # total_runtime = time.time() - start_time

    # print(time.strftime("%H:%M:%S", time.gmtime(total_runtime)))
