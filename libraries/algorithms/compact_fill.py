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

        course_id = 0
        course_name = list(courses)
        lecture_count: int = courses[course_name[course_id]].number_of_activities()

        # insert all activities in schedule.
        for day_name, day in self.schedule.days.items():
            for index, slot in enumerate(day.slots):
                lecture_count -= 1
                # Check if lecture count is 0 or 29
                if lecture_count == 0:
                    course_id += 1
                self.schedule.insert_activity(day_name, index, activity)

                if course_id == 29:
                    # quit condition
                    return self.schedule
                else:
                    lecture_count: int = courses[
                        course_name[course_id]
                    ].number_of_activities()

                students = list(activity.course.students.values())
                for student in students:
                    activity.add_student(student)

        return self.schedule
