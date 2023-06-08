# This is a (temporary file) meant to show the functionality of the classes in activity.py, calender.py and course.py
# Contents of this file will probably be transferred to main.py or ./helpers/ in the near future
# 08-06-2023

import pandas as pd
from course import Course
from schedule import ScheduleSlot, Schedule
from activity import Activity

# read data 
df_vakken = pd.read_csv("../data/vakken.csv")

# print(df_vakken)
 
# create courses dict (key=coursename, value=Course obj)
courses = {}
for index, row in df_vakken.iterrows():

    courses[row['Vak']] = Course(
        name          = row['Vak'],
        lectures      = row['#Hoorcolleges'], 
        workgroups    = row['#Werkcolleges'], 
        max_workgroup = row['Max. stud. Werkcollege'],
        practicals    = row['#Practica'], 
        max_practical = row['Max. stud. Practicum'],
        expected      = row['Verwacht']
        )

# add activity objects to courses
for course in courses:
    course = courses[course]

    # add lectures
    course.lectures = [Activity(course=course.name, category=f'lecture{i+1}', capacity=course.expected) for i in range(course.lectures)]

    # add practicals
    course.practicals = [Activity(course=course.name, category=f'practical{i+1}', capacity=course.max_practical) for i in range(course.practicals)]

    # add workgroups
    course.workgroups = [Activity(course=course.name, category=f'workgroup{i+1}', capacity=course.max_workgroup) for i in range(course.workgroups)]

# put all activities in a list
all_activities = []
for course in courses:
    course = courses[course]
    for act in course.all_activities():
        all_activities.append(act)

# create all empty timeslots
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
halls = {"A1.04": 41, "A1.06":22, "A1.08":20, "A1.10":56, "B0.201":48, "C0.110":117, "C1.112":60}
timeslots = [str(i) for i in range(9, 19, 2)]
slots = []
for day in weekdays:
    for timeslot in timeslots:
        for hall in halls:
            slots.append(ScheduleSlot(day, timeslot, hall, halls[hall]))

# create empty schedule
s = Schedule(slots)

# dump all activities in schedule (accounting for room capacity!)
for activity in all_activities:
    s.insert_activity(activity)

# print schedule
print(s.__repr__)

# other examples
df = pd.DataFrame(s.as_list_of_dicts())
print("THIS IS A DATAFRAME OF THE WHOLE SCHEDULE WHEN ACCOUNTING FOR ROOM SIZE: \n", df)

room_scheme = df[df.room == 'A1.04']
print("THESE ARE ALL ACTIVITIES IN A1.04 ACROSS THE WHOLE WEERK: \n", room_scheme)

day_schema = df[df.day == 'Monday']
print("THESE ARE ALL ACTIVITIES ON MONDAY:\n", day_schema)