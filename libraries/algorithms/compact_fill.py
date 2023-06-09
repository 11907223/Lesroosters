
def fill_schedule(courses, schedule):
    # put all activities in a list
    all_activities = []
    for course in courses:
        course = courses[course]
        for activity in course.activities():
            all_activities.append(activity)

    # insert all activities in schedule (accounting for room capacity!)
    for activity in all_activities:
        schedule.insert_activity(activity)
        students = courses[activity.course].students.values()
        for student in students:
            activity.add_student({student.index: student})