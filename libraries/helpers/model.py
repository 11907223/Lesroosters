from libraries.classes.schedule import Schedule
from libraries.helpers.load_data import load_courses, load_students
from libraries.algorithms.random import Random

class Model:
    def __init__(self) -> None:
        self.courses = load_courses()
        self.schedule = Random(Schedule(), self.courses).run()
        self.students = load_students(self.courses)

    def add_activity_to_schedule(self, activity: str):
        pass

    def add_student_to_activity(self, student: str, activity: str):
        pass

    def call_algorithm(self, algorithm):
        pass
        # if algorithm == "random":
            # random_schedule(self.courses, self.schedule)

    def translate_schedule_to_model(self):
        schedule_model = {}
        for index, entry in enumerate(self.schedule.as_list_of_dicts()):
            activity = entry['activity']
            course = entry['course']
            schedule_model[index] = {'activity': activity, 'course': course}
        
        students_per_activity = {}
        for day in self.schedule.days.values():
            for slot in day.slots:
                if slot.activity is not None:
                    students_per_activity[f"{slot.activity.course.name} {slot.activity.category}"] = slot.activity.students
        print(students_per_activity)
