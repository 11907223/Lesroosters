"""
Flask app to visualize a university scheduling tool.
"""
from libraries.algorithms.randomise import Random
from libraries.algorithms.greedy import Greedy
from libraries.classes.model import Model
from libraries.helpers.load_data import load_courses, load_students, load_halls
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template

app = Flask(__name__)

# knop algoritme kiezen
# lijst studenten + aantal vakken per student
# lijst vakken, aant studenten, aant hoorcolleges, werkcolleges, practica


@app.route("/")
def index():
    """Renders homepage with a random schedule."""

    # Load all data
    courses = load_courses()
    students = load_students(courses)
    halls = load_halls()

    # Create a dictionary with weekdays and timeslots
    weekdays = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday"}
    timeslots = {0: "9", 1: "11", 2: "13", 3: "15", 4: "17"}

    # Initialize model and run random algorithm
    model = Model(courses, students, halls)
    # random_schedule = Random(model)
    greedy_schedule = Greedy(model)
    schedule_solution = greedy_schedule.run()

    # Create a dict of the solution
    schedule_dict = create_dict(schedule_solution, halls, weekdays, timeslots)

    # Create a list of all students
    students_list = create_student_list(students)

    # Calcualte penalty
    penalty = schedule_solution.total_penalty()

    return render_template(
        "index.html",
        weekdays=weekdays,
        schedule=schedule_dict,
        score=penalty,
        students=students_list,
    )


def create_dict(model: Model, halls: dict, weekdays: dict, timeslot: dict) -> dict:
    """Create a dict from a model object."""

    # Create an empty dictionary
    schedule_dict: dict = {
        time: {day: [] for day in weekdays.values()} for time in timeslot.values()
    }

    # Fill the empty schedule dict with information from the class
    for index, activity in model.solution.items():
        info = model.translate_index(index)
        day = weekdays[info["day"]]
        time = timeslot[info["timeslot"]]
        hall = halls[info["hall"]]
        if activity[0]:
            schedule_dict[time][day].append([activity[0], activity[1], hall])

    return schedule_dict


def create_student_list(students: dict) -> list:
    """Create a list of all students."""
    students_list = []

    for student in students.values():
        student_info = (
            f"{student.first_name} {student.last_name}, {student.student_number}"
        )
        students_list.append(student_info)

    return students_list
