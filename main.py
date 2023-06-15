from libraries.helpers.load_data import load_courses, load_students
from libraries.algorithms.random import Random
from libraries.classes.schedule import Schedule
from libraries.classes.penalty import Penalty
from libraries.helpers.model import Model
import pandas as pd
import time


if __name__ == "__main__":
    courses = load_courses()
    students = load_students(courses)
    schedule = Schedule()

    # # other examples
    # df = pd.DataFrame(schedule.as_list_of_dicts())
    # print(
    #     "THIS IS A DATAFRAME OF THE WHOLE SCHEDULE WHEN ACCOUNTING FOR ROOM SIZE: \n",
    #     df,
    # )

    s = Model(courses, students, schedule)
    print(s.get_empty_model())
    print(s.translate_index(144))

    start_time = time.time()

    # with open("baseline.txt", "a+") as file:
    #     for _i in range(100000):
    #         random_schedule = Random(schedule, courses)
    #         random_schedule = random_schedule.run()
    #         penalty = Penalty(random_schedule)
    #         file.write(f"{penalty.total()}\n")

    total_runtime = time.time() - start_time

    print(time.strftime("%H:%M:%S", time.gmtime(total_runtime)))
