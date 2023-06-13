from libraries.classes.schedule import Schedule
from libraries.helpers.load_data import load_courses
import random


def random_schedule():
    courses = load_courses()

    # put all activities in a list
    all_activities = []
    for course_name in courses:
        course = courses[course_name]
        for act in course.activities():
            all_activities.append(act)
    # create empty schedule
    s = Schedule("data")

    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    for activity in all_activities:
        inserted_all_courses = False
        # insert activity at random point
        while not inserted_all_courses:
            index = random.random() * (len(s.days[weekdays[1]].slots) - 1)
            weekday = random.choice(weekdays)
            inserted_all_courses = s.insert_activity(weekday, int(index), activity)
    return s
