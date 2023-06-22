import pandas as pd
import csv
from libraries.classes.course import Course
from libraries.classes.activity import Activity
from libraries.classes.student import Student
from libraries.classes.hall import Hall


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
    for _index, course in df_courses.iterrows():
        courses[course["Vak"]] = Course(course_name=course["Vak"])
        for activities in init_activities(courses[course["Vak"]], course):
            for activity_name, activity_set in activities.items():
                for activity in activity_set:
                    courses[course["Vak"]].add_activity(activity_name, activity)

    return courses


def init_activities(course_obj: Course, course: pd.Series):
    """Generate activity objects in list for a course.

    Args:
        course_obj (Course): Course object.
        course (pd.Series): Row containing course data.

    Returns:
        tuple: list of lectures, list of tutorials, list of practicals.
    """
    n_lectures = course["#Hoorcolleges"]
    n_practicals = course["#Practica"]
    n_tutorials = course["#Werkcolleges"]

    # Add lectures.
    lectures = {
        "lectures": {Activity(
            course=course_obj, category=f"lecture {i+1}", capacity=course["Verwacht"]
        )
        for i in range(n_lectures)}
    }

    # Add practicals.
    practicals = {
        "practicals": {Activity(
            course=course_obj,
            category=f"practical {i+1}",
            capacity=course["Max. stud. Practicum"],
        )
        for i in range(n_practicals)}
    }
    # Add tutorials.
    tutorials = {
        "tutorials": {Activity(
            course=course_obj,
            category=f"tutorial {i+1}",
            capacity=course["Max. stud. Werkcollege"],
        )
        for i in range(n_tutorials)}
    }

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
    for index, student in df_students.iterrows():
        subjects = load_subjects(courses, student)
        students[index] = Student(
            index=index,
            first_name=student["Voornaam"],
            last_name=student["Achternaam"],
            student_number=student["Stud.Nr."],
            courses=subjects,
        )

        update_course(courses, students[index])
    return students


def load_subjects(courses, student):
    return {
        student[f"Vak{i+1}"]: courses[student[f"Vak{i+1}"]]
        for i in range(5)
        if isinstance(student[f"Vak{i+1}"], str)
    }


def update_course(courses: "dict[str, Course]", student: Student):
    for course in student.courses.keys():
        courses[course].add_student(student)


def load_halls(path: str = "data"):
    # read halls from csv
    halls_raw = [
        hall
        for hall in csv.DictReader(
            open(f"{path}/zalen.csv", mode="r", encoding="utf-8-sig")
        )
    ]

    # create a dictionary with halls and their capacity
    halls = {}
    for index, hall in enumerate(halls_raw):
        hall_name, capacity = hall.values()
        halls.update({index: Hall(hall_name, int(capacity))})

    return halls