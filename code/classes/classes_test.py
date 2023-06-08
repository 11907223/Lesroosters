""" This is a (temporary file) meant to show the functionality of the classes in activity.py, calender.py and course.py

Contents of this file will probably be transferred to main.py or ./helpers/ in the near future

08-06-2023
"""

import pandas as pd
import csv
from course import Course
from schedule import ScheduleSlot, Schedule
from activity import Activity

# read data
df_vakken = pd.read_csv("../../data/vakken.csv")

# create courses dict (key=coursename, value=Course obj)
courses = {}
for index, row in df_vakken.iterrows():
    courses[row["Vak"]] = Course(
        name=row["Vak"],
        lectures=row["#Hoorcolleges"],
        tutorials=row["#Werkcolleges"],
        max_tutorial_capacity=row["Max. stud. Werkcollege"],
        practicals=row["#Practica"],
        max_practical_capacity=row["Max. stud. Practicum"],
        expected=row["Verwacht"],
    )

# add activity objects to courses
for course in courses:
    course = courses[course]

    # add lectures
    course.lectures = [
        Activity(course=course.name, category=f"lecture{i+1}", capacity=course.expected)
        for i in range(course.lectures)
    ]

    # add practicals
    course.practicals = [
        Activity(
            course=course.name,
            category=f"practical{i+1}",
            capacity=course.max_practical_capacity,
        )
        for i in range(course.practicals)
    ]

    # add workgroups
    course.tutorials = [
        Activity(
            course=course.name,
            category=f"tutorial{i+1}",
            capacity=course.max_tutorial_capacity,
        )
        for i in range(course.tutorials)
    ]

# put all activities in a list
all_activities = []
for course in courses:
    course = courses[course]
    for act in course.all_activities():
        all_activities.append(act)

# create all empty timeslots
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
halls_raw = [hall for hall in csv.DictReader(open("../../data/zalen.csv", mode='r', encoding='utf-8-sig'))]
halls = {}
for hall in halls_raw:
    hall_id, capacity = hall.values()
    halls.update({hall_id: int(capacity)})

timeslots = [str(i) for i in range(9, 19, 2)]
slots = []
for day in weekdays:
    for timeslot in timeslots:
        for hall in halls:
            slots.append(ScheduleSlot(day, timeslot, hall, halls[hall]))

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
print("THESE ARE ALL ACTIVITIES IN A1.04 ACROSS THE WHOLE WEERK: \n", room_scheme)

day_schema = df[df.day == "Monday"]
print("THESE ARE ALL ACTIVITIES ON MONDAY:\n", day_schema)
