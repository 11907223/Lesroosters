import pandas as pd
from libraries.classes.course import Course
from libraries.classes.activity import Activity
from libraries.classes.student import Student


def load_courses(path: str = "data"):
    """Load courses from csv to a dictionary.

    Args:
        path (str): path of csv to load.
            Defaults to "/data"

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
    n_lectures = course["#Hoorcolleges"]
    n_practicals = course["#Practica"]
    n_tutorials = course["#Werkcolleges"]

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


def load_students(courses, path: str = "data"):
    """Load students from file to a dictionary.

    Args:
        courses (dict): Dictionary of all courses.
        path (str): Path of csv to load.
            Defaults to "/data"

    Returns:
        dict: Contains courses and their activities.
          key = student index, value = Student obj.
    """
    df_students = pd.read_csv(f"{path}/studenten_en_vakken.csv")

    students = {}
    for index, row in df_students.iterrows():
        subjects = {row[f"Vak{i+1}"]: courses[row[f"Vak{i+1}"]] for i in range(5) if isinstance(row[f"Vak{i+1}"], str)}
        students[index] = Student(
            first_name=row["Voornaam"],
            last_name=row["Achternaam"],
            id=row["Stud.Nr."],
            courses=subjects
        )

    return students
