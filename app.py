"""
Flask app to visualize a university scheduling tool.
"""

from dotenv import load_dotenv

load_dotenv()


from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    timeslots = [
        "09:00-11:00",
        "11:00-13:00",
        "13:00-15:00",
        "15:00-17:00",
        "17:00-19:00",
    ]
    return render_template("index.html", weekdays=weekdays, timeslots=timeslots)
