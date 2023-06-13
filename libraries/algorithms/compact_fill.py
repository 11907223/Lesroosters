from copy import deepcopy


def fill_schedule(courses, schedule):
    # put all activities in a list
    all_activities = []
    for course in courses:
        course = courses[course]
        for activity in course.activities():
            all_activities.append(activity)

    # insert all activities in schedule (accounting for room capacity!)
    for index, activity in enumerate(all_activities):
        schedule.insert_activity(activity, index)
        students = courses[activity.course].students.values()
        for student in students:
            activity.add_student({student.index: student})


class compact_fill:
    def __init__(self, schedule) -> None:
        # TODO convert to model (dict, acts(str))
        # add act dict with students
        self.schedule = deepcopy(schedule)

    def fill(self, courses):
        all_activities = []
        for course_name in courses:
            course = courses[course_name]
            for activity in course.activities():
                all_activities.append(activity)

        # insert all activities in schedule.
        for activity in all_activities:
            for day in self.schedule.days:
                index, _slot = enumerate(day)
                self.schedule.insert_activity(day, index, activity)
                students = activity.course.students.values()
                for student in students:
                    activity.add_student({student.index: student})

        return self.schedule