from libraries.classes.schedule import Schedule
from libraries.classes.course import Course
from libraries.helpers.load_data import load_courses
import random
import copy

def random_schedule():
    courses = load_courses()

    # put all activities in a list
    all_activities = []
    for course_name in courses:
        course = courses[course_name]
        for act in course.activities():
            all_activities.append(act)
    # create empty schedule
    s = Schedule("data")

    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    for activity in all_activities:
        inserted_all_courses = False
        # insert activity at random point
        while not inserted_all_courses:
            index = random.random() * (len(s.days[weekdays[1]].slots))
            weekday = random.choice(weekdays)
            inserted_all_courses = s.insert_activity(weekday, int(index), activity)
            students = activity.course.students
            print(students)
            for student in students:
                    activity.add_student(student)
                    print(activity.students)
    return s

class Random:
    def __init__(self, empty_schedule, courses):
        self.schedule = copy.deepcopy(empty_schedule)
        self.activities = self.load_activities(courses)

    def load_activities(self, courses):
        # put all activities in a list
        all_activities = []

        for course_name in courses:
            course = courses[course_name]
            student_dict = course.students

            for act in course.activities():
                all_activities.append(act)
                act.add_students(student_dict)

        return all_activities
    
    # def assign_students(self, courses):
    #     # add students to activities
    #     for course in courses:
    #         student_dict = courses[course].students


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