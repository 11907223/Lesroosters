"""
Flask app to visualize a university scheduling tool.
"""
from libraries.algorithms.random import random_schedule
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

    # Create a list with weekdays
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    # Create an empty dictionary
    schedule_dict = {
        time: {day: [] for day in weekdays} for time in ["9", "11", "13", "15", "17"]
    }
    print(schedule_dict)
    # Initialize a random schedule
    schedule = random_schedule()

    students = []

    # Fill the empty schedule dict with information from the class
    for slot in schedule.slots:
        if slot.activity:
            schedule_dict[slot.time][slot.day].append([slot.activity.course, slot.room])
            students.append(slot.activity.course.students)

    malus_points = -50

    return render_template(
        "index.html",
        weekdays=weekdays,
        schedule=schedule_dict,
        score=malus_points,
        students=students,
    )
