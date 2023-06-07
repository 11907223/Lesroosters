import pandas as pd
import sys

sys.path.append("./helpers/")
from schedule import Schedule()
from display import display_schedule


if __name__ == "__main__":

    schedule = Schedule(pd.read_csv("../data/zalen.csv"))
    schedule.dump_courses_in_schedule(pd.read_csv("../data/vakken.csv"))
    df = pd.DataFrame(schedule.schedule)

    display_schedule(df)
