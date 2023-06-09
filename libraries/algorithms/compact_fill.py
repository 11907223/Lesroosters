
def fill_schedule(courses, schedule):
    # put all activities in a list
    activities = []
    for course in courses:
        course = courses[course]
        for activity in course.activities():
            activities.append(activity)

    # insert all activities in schedule (accounting for room capacity!)
    for activity in activities:
        schedule.insert_activity(activity)