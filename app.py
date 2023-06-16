"""
Flask app to visualize a university scheduling tool.
"""
from libraries.algorithms.randomise import Random
from libraries.classes.penalty import Penalty
from libraries.classes.schedule import Schedule
from libraries.classes.student import Student
from libraries.helpers.load_data import load_courses, load_students
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
    schedule = Schedule()

    random_schedule = Random(schedule, courses)
    random_schedule = random_schedule.run()

    # Create a list with weekdays
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    # Create an empty dictionary
    schedule_dict = {
        time: {day: [] for day in weekdays} for time in ["9", "11", "13", "15", "17"]
    }

    students = []

    # Fill the empty schedule dict with information from the class
    for day in random_schedule.days.items():
        for slot in day[1].slots:
            if slot.activity:
                schedule_dict[slot.time][slot.day].append(
                    [slot.activity.course.name, slot.room]
                )
                student_objects = slot.activity.students.values()

                for student in student_objects:
                    student_info = f"{student.first_name} {student.last_name}, {student.student_number}"
                    students.append(student_info)

    penalty = Penalty(random_schedule)

    evening_penalty = penalty.total()

    return render_template(
        "index.html",
        weekdays=weekdays,
        schedule=schedule_dict,
        score=evening_penalty,
        students=students,
    )
