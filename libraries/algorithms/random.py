from libraries.classes.schedule import Schedule
from libraries.classes.course import Course
from libraries.helpers.load_data import load_courses
import random
import copy

class Random:
    def __init__(self, empty_schedule, courses):
        self.schedule = copy.deepcopy(empty_schedule)
        self.activities = self.load_activities(courses)

    def load_activities(self, courses):
        # put all activities in a list & add students to activities
        all_activities = []

        for course_name in courses:
            course = courses[course_name]
            student_dict = course.students

            for act in course.activities():
                all_activities.append(act)

                # add students to activity
                act.add_students(student_dict)

                # add activity to students
                for student in student_dict.values():
                    student.add_activity(act)
        return all_activities
    
    def run(self):
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        for activity in self.activities:
            inserted_all_courses = False
            # insert activity at random point
            while not inserted_all_courses:
                index = random.random() * (len(self.schedule.days[weekdays[1]].slots))
                weekday = random.choice(weekdays)
                inserted_all_courses = self.schedule.insert_activity(weekday, int(index), activity)
        return self.schedule