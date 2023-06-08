import pandas as pd

from helpers.load_data import load_courses


if __name__ == "__main__":
    courses = load_courses(path="../data")
    print(courses)
