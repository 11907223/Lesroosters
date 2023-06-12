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
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    schedule_list = {
        time: {
            day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        }
        for time in ["9", "11", "13", "15", "17"]
    }

    schedule = random_schedule()

    print("EMPTY LIST!!!")
    print(schedule_list)
    for slot in schedule.days:
        if slot.activity:
            schedule_list[slot.time][slot.day].append([slot.activity.course, slot.room])

    print(schedule_list)

    return render_template(
        "index.html",
        weekdays=weekdays,
        schedule=schedule_list,
    )
