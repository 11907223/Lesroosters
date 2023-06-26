from libraries.classes.model import Model
from jinja2 import Template


def create_dict(model: Model) -> dict:
    """Create a dict from a model object."""
    # Create a dictionary with weekdays and timeslots
    weekdays = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday"}
    timeslot = {0: "9", 1: "11", 2: "13", 3: "15", 4: "17"}
    halls = model.halls

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

    return schedule_dict


def read_html_file(file_path):
    with open(file_path, "r") as file:
        html_content = file.read()

    return html_content


def visualize(model: Model):
    weekdays = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday"}

    schedule_dict = create_dict(model)

    penalty = model.calc_total_penalty()

    # HTML template
    html_string = read_html_file("helpers/template.html")

    # Create a Jinja2 template object
    template = Template(html_string)

    # Render the template with data
    rendered_html = template.render(
        weekdays=weekdays,
        schedule=schedule_dict,
        score=penalty,
    )

    # Output the rendered HTML
    print(rendered_html)
