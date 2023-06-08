import pandas as pd
import sys

sys.path.append("helpers")
from load_data import load_courses


if __name__ == "__main__":
    courses = load_courses(path="../data/vakken.csv")
    print(courses)
