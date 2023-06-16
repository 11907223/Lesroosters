import libraries.helpers.load_data as ld
from libraries.algorithms.random import Random
from libraries.classes.model import Model
import pandas as pd
import time


if __name__ == "__main__":
    courses = ld.load_courses()
    students = ld.load_students(courses)
    halls = ld.load_halls()

    s = Model(courses, students, halls)
    print(s.init_model((None, None)))
    print(s.participants)
    print(s.init_student_model()[("Webprogrammeren en databases", "lecture 2")])
    print(s.check_index_is_empty(2))

    r = Random(s).run()
    print(r.model)
    # start_time = time.time()

    # with open("baseline.txt", "a+") as file:
    #     for _i in range(100000):
    #         random_schedule = Random(schedule, courses)
    #         random_schedule = random_schedule.run()
    #         penalty = Penalty(random_schedule)
    #         file.write(f"{penalty.total()}\n")

    # total_runtime = time.time() - start_time

    # print(time.strftime("%H:%M:%S", time.gmtime(total_runtime)))

    print(s.get_highest_students(3))
