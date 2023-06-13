from libraries.classes.schedule import Schedule
from libraries.helpers.load_data import load_courses, load_students
from libraries.algorithms.random import Random


class Model:
    def __init__(self) -> None:
        self.schedule = random_schedule()
        self.courses = load_courses()
        self.students = load_students(self.courses)

    def add_activity_to_schedule(self, activity: str):
        pass

    def add_student_to_activity(self, student: str, activity: str):
        pass

    def call_algorithm(self, algorithm):
        if algorithm == "random":
            random_schedule(self.courses, self.schedule)

    def translate_schedule_to_model(self):
        schedule_model = {}
        for index, entry in enumerate(self.schedule.as_list_of_dicts()):
            activity = entry["activity"]
            course = entry["course"]
            schedule_model[index] = {"activity": activity, "course": course}
        print(schedule_model)

        students_per_activity = {}

        for course in self.courses.values():
            for activity in course.activities():
                students_per_activity[
                    f"{activity.course.name} {activity.category}"
                ] = activity.students
        print(students_per_activity)
