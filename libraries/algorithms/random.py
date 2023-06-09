import pandas as pd
import csv
from libraries.classes.schedule import ScheduleSlot, Schedule
from libraries.helpers.load_data import load_courses


def random_schedule():
    courses = load_courses()

    # add student

    # put all activities in a list
    all_activities = []
    for course in courses:
        course = courses[course]
        for act in course.all_activities():
            all_activities.append(act)

    # read halls from csv
    halls_raw = [
        hall
        for hall in csv.DictReader(
            open("../../data/zalen.csv", mode="r", encoding="utf-8-sig")
        )
    ]

    # create a dictionary with halls and their capacity
    halls = {}
    for hall in halls_raw:
        hall_id, capacity = hall.values()
        halls.update({str(hall_id): int(capacity)})

    # create all empty timeslots
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    timeslots = [str(i) for i in range(9, 19, 2)]
    slots = []
    for day in weekdays:
        for timeslot in timeslots:
            for hall_id, capacity in halls.items():
                slots.append(ScheduleSlot(day, timeslot, hall_id, capacity))

    # create empty schedule
    s = Schedule(slots)

    # randomly insert all activities in schedule (accounting for room capacity!)
    for activity in all_activities:
        s.insert_activity(activity)

    return s
