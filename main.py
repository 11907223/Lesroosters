from libraries.helpers.load_data import load_courses, load_students
from libraries.algorithms.random import Random
from libraries.classes.schedule import Schedule
from libraries.helpers.model import Model
import pandas as pd
import time


if __name__ == "__main__":
    courses = load_courses()
    students = load_students(courses)
    # schedule = Random(Schedule(), courses).run()

    # # other examples
    # df = pd.DataFrame(schedule.as_list_of_dicts())
    # print(
    #     "THIS IS A DATAFRAME OF THE WHOLE SCHEDULE WHEN ACCOUNTING FOR ROOM SIZE: \n",
    #     df,
    # )

    s = Model(courses, students, 6)
    print(s.init_model((None, None)))
    print(s.participants)
    print(s.init_student_model()[("Webprogrammeren en databases", "lecture 2")])
    print(s.check_index_is_empty(2))

    # start_time = time.time()

    # with open("baseline.txt", "a+") as file:
    #     for _i in range(100000):
    #         random_schedule = Random(schedule, courses)
    #         random_schedule = random_schedule.run()
    #         penalty = Penalty(random_schedule)
    #         file.write(f"{penalty.total()}\n")

    # total_runtime = time.time() - start_time

    # print(time.strftime("%H:%M:%S", time.gmtime(total_runtime)))

    print(s.total_penalty())
