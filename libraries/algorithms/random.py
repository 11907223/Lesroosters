import pandas as pd
import csv
from libraries.classes.schedule import Hall_slot, Schedule
from libraries.helpers.load_data import load_courses
from random import random

def random_schedule():
    courses = load_courses()

    # put all activities in a list
    all_activities = []
    for course in courses:
        course = courses[course]
        for act in course.activities():
            all_activities.append(act)

    # create empty schedule
    s = Schedule("data")

    
    for activity in all_activities:
        
        insertion = False
        # insert activity at random point
        while not insertion:
            index = random()*(len(s.days)-1)
            insertion = s.insert_activity(int(index), activity)
    return s
