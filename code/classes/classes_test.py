""" This is a (temporary file) meant to show the functionality of the classes in activity.py, calender.py and course.py

Contents of this file will probably be transferred to main.py or ./helpers/ in the near future

08-06-2023
"""

import pandas as pd
import csv
from malus import ScheduleSlot, Schedule
from load_data import load_courses


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

# insert all activities in schedule (accounting for room capacity!)
for activity in all_activities:
    s.insert_activity(activity)

# print schedule
print(s.__repr__)

# other examples
df = pd.DataFrame(s.as_list_of_dicts())
print("THIS IS A DATAFRAME OF THE WHOLE SCHEDULE WHEN ACCOUNTING FOR ROOM SIZE: \n", df)

room_scheme = df[df.room == "A1.04"]
print("THESE ARE ALL ACTIVITIES IN A1.04 ACROSS THE WHOLE WEEK: \n", room_scheme)

day_schema = df[df.day == "Monday"]
print("THESE ARE ALL ACTIVITIES ON MONDAY:\n", day_schema)
