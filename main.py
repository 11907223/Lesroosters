import libraries.helpers.load_data as ld
from libraries.algorithms.randomise import Random, random_algorithm
from libraries.classes.model import Model
# from libraries.algorithms.greedy import Greedy

if __name__ == "__main__":
    courses = ld.load_courses()
    students = ld.load_students(courses)
    halls = ld.load_halls()

    empty_model = Model(courses, students, halls)
    random_model = Random(empty_model).run()
    # print(s.get_highest_students(3))
    print(random_model.solution)
    print(random_model.total_penalty())

    # start_time = time.time()

    print(random_model.total_penalty())

    # _________________________RANDOM ALGORITHM_______________________
    iterations = 1
    random_solution   = random_algorithm(iterations, empty_model)

    print('THE BEST SCHEDULE FOUND WHEN USING RANDOM:\n', random_solution.solution, '\n POINTS: ', random_solution.total_penalty())
    # ________________________________________________________________

    # ________________________GREEDY ALGORITHM________________________
    # greedy_solution = Greedy(s).run()
    # print('THE BEST SCHEDULE FOUND WHEN USING GREEDY:\n', greedy_solution.model, '\n POINTS: ', greedy_solution.total_penalty())
    # ________________________________________________________________


    # with open("baseline.txt", "a+") as file:
    #     for _i in range(100000):
    #         random_schedule = Random(schedule, courses)
    #         random_schedule = random_schedule.run()
    #         penalty = Penalty(random_schedule)
    #         file.write(f"{penalty.total()}\n")

    # total_runtime = time.time() - start_time

    # print(time.strftime("%H:%M:%S", time.gmtime(total_runtime)))