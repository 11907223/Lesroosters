import pandas as pd
import sys

sys.path.append("./helpers/")
from schedule import fill_prototype_schedule, init_empty_schedule


def main():
    df_vakken = pd.read_csv("./data/vakken.csv")
    df_zalen = pd.read_csv("./data/zalen.csv")

    result = fill_prototype_schedule(df_vakken)
    print(result)


main()
