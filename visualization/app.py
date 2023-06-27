"""
Flask app to visualize a university scheduling tool.
"""
from libraries.algorithms.randomise import Random
from libraries.algorithms.greedy import Greedy
from libraries.algorithms.beam_search import BeamSearch
from libraries.classes.model import Model
from libraries.helpers.load_data import load_courses, load_students, load_halls
from dotenv import load_dotenv
import os
import ast

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), "visualization/.env")
load_dotenv(dotenv_path)

from flask import Flask, render_template

app = Flask(__name__)


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

    schedule_solution = read_dict_from_txt()
    print(schedule_solution)
    # Create a dict of the solution
    schedule_dict = create_dict(schedule_solution, halls, weekdays, timeslots)

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

    count = 0

    # Fill the empty schedule dict with information from the class
    for index, activity in model.solution.items():
        info = model.translate_index(index)
        day = weekdays[info["day"]]
        time = timeslot[info["timeslot"]]
        hall = halls[info["hall"]]
        if activity[0]:
            schedule_dict[time][day].append([activity[0], activity[1], hall])
            count += 1

    print("VAKKEN INGEROOSTERD ", count)
    return schedule_dict


def read_dict_from_txt() -> dict:
    schedule_dict = {}

    # Open the text file for reading
    with open(
        "/Users/elisevaniterson/Documents/Programming/lesroosters/results/model_result.txt",
        "r",
    ) as file:
        # Read the content of the file
        file_content = file.read()

        # Evaluate the content as a literal expression to get the dictionary
        schedule_dict = ast.literal_eval(file_content)

    # Return the resulting dictionary
    return schedule_dict
