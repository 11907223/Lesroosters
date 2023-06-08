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
        lectures, tutorials, practicals = init_activities(row)
        courses[row["Vak"]] = Course(
            name=row["Vak"],
            lectures=lectures,
            tutorials=tutorials,
            max_tutorial_capacity=row["Max. stud. Werkcollege"],
            practicals=practicals,
            max_practical_capacity=row["Max. stud. Practicum"],
            expected=row["Verwacht"],
        )

    return courses


def init_activities(course):
    """Generate activity objects in list for a course.
    
    Args:
        course (pd.Series): Row containing course data.

    Returns:
        tuple: list of lectures, list of tutorials, list of practicals.
    """
    name = course["Vak"]
    n_lectures = course["#Hoorcollege"]
    n_practicals = course["#Practicals"]
    n_tutorials = course["#Werkgroepen"]

    # Add lectures.
    lectures = [
        Activity(course=name, category=f"lecture {i+1}", capacity=course["Verwacht"])
        for i in range(n_lectures)
    ]

    # Add practicals.
    practicals = [
        Activity(
            course=name,
            category=f"practical {i+1}",
            capacity=course["Max. stud. Practicum"],
        )
        for i in range(n_practicals)
    ]

    # Add tutorials.
    tutorials = [
        Activity(
            course=name,
            category=f"tutorial {i+1}",
            capacity=course["Max. stud. Werkcollege"],
        )
        for i in range(n_tutorials)
    ]

    return lectures, tutorials, practicals
