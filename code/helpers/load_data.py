import pandas as pd

from classes.course import Course
from classes.activity import Activity


def load_courses(path: str = "../../data"):
    """Load courses from file to a dictionary.

    Args:
        path (str): path of courses to load.
            Defaults to "../../data"

    Returns:
        dict: Contains courses and their activities.
          key = coursename, value = Course obj.
    """
    d_type = {
        "Vak": str,
        "#Hoorcolleges": int,
        "#Werkcolleges": int,
        "Max stud. Werkcollege": int,
        "#Practica": int,
        "Max stud. Practicum": int,
        "Verwacht": int,
    }
    df_courses = pd.read_csv(f"{path}/vakken.csv", dtype=d_type)

    courses = {}
    for _index, row in df_courses.iterrows():
        courses[row["Vak"]] = Course(
            name=row["Vak"],
            lectures=row["#Hoorcolleges"],
            tutorials=row["#Werkcolleges"],
            max_tutorial_capacity=row["Max. stud. Werkcollege"],
            practicals=row["#Practica"],
            max_practical_capacity=row["Max. stud. Practicum"],
            expected=row["Verwacht"],
        )

    for course in courses.values():
        init_activities(course)

    return courses


def init_activities(course):
    """Add activity objects to course."""

    # Add lectures
    course.lectures = [
        Activity(
            course=course.name, category=f"lecture {i+1}", capacity=course.expected
        )
        for i in range(course.lectures)
    ]

    # Add practicals.
    course.practicals = [
        Activity(
            course=course.name,
            category=f"practical {i+1}",
            capacity=course.max_practical_capacity,
        )
        for i in range(course.practicals)
    ]

    # Add tutorials.
    course.tutorials = [
        Activity(
            course=course.name,
            category=f"tutorial {i+1}",
            capacity=course.max_tutorial_capacity,
        )
        for i in range(course.tutorials)
    ]

    return course
