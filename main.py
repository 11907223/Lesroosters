from libraries.helpers.load_data import load_courses, load_students
from libraries.algorithms.random import random_schedule
from libraries.classes.schedule import Schedule
from libraries.algorithms.compact_fill import compact_fill
from libraries.classes.penalty import Penalty
import pandas as pd


if __name__ == "__main__":
    courses = load_courses()
    students = load_students(courses)
    schedule = Schedule()

    schedule = random_schedule()
    compact = compact_fill(schedule)
    compact.fill(courses)
    print(pd.DataFrame(compact.fill(courses).as_list_of_dicts()))

    print(schedule)
    # other examples
    df = pd.DataFrame(schedule.as_list_of_dicts())
    print(
        "THIS IS A DATAFRAME OF THE WHOLE SCHEDULE WHEN ACCOUNTING FOR ROOM SIZE: \n",
        df,
    )

    room_scheme = df[df.room == "A1.04"]
    print("THESE ARE ALL ACTIVITIES IN A1.04 ACROSS THE WHOLE WEEK: \n", room_scheme)

    day_schema = df[df.day == "Monday"]
    print("THESE ARE ALL ACTIVITIES ON MONDAY:\n", day_schema)

    score = Penalty(schedule)

    print(score.capacity_penalty())
    # print(schedule.as_list_of_dicts())
