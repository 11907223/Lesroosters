"""
Flask app to visualize a university scheduling tool.
"""
from libraries.algorithms.randomise import Random
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

    courses = load_courses()
    students = load_students(courses)
    halls = load_halls()
    model = Model(courses, students, halls)

    random_schedule = Random(model)
    random_schedule = random_schedule.run()

    # student_objects = slot.activity.students.values()

    # for student in student_objects:
    #     student_info = (
    #         f"{student.first_name} {student.last_name}, {student.student_number}"
    #     )
    #     students.append(student_info)

    penalty = model.total_penalty()

    return render_template(
        "index.html",
        weekdays=weekdays,
        schedule=schedule_dict,
        score=penalty,
        students=students,
    )


def create_dict(model: Model(), courses, students, halls) -> dict:
    # Create a list with weekdays
    weekdays = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday"}
    timeslot = {0: "9", 1: "11", 2: "13", 3: "15", 4: "17"}
    # Create an empty dictionary
    schedule_dict = {
        time: {day: [] for day in weekdays.values()} for time in timeslot.values()
    }

    students = []

    # Fill the empty schedule dict with information from the class
    for index, activity in random_schedule.model.items():
        info = random_schedule.translate_index(index)
        day = weekdays[info["day"]]
        time = timeslot[info["timeslot"]]
        hall = halls[info["hall"]]
        if activity[0]:
            schedule_dict[time][day].append([activity[0], activity[1], hall])
