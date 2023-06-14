from libraries.classes.schedule import Schedule
from libraries.helpers.load_data import load_courses, load_students
from libraries.algorithms.random import Random

class Model:
    def __init__(self) -> None:
        self.courses = load_courses()
        self.students = load_students(self.courses)
        self.schedule = Random(Schedule(), self.courses).run()

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
            day = entry['day']
            local_index = index % 29
            activity = entry['activity']
            course = entry['course']

            if day not in schedule_model:
                schedule_model[day] = {}

            if 'index' not in schedule_model[day]:
                schedule_model[day]['index'] = {}

            schedule_model[day]['index'][local_index] = {'course': course, 'activity': activity}

        students_in_activities = self.students_to_model()

        return schedule_model, students_in_activities

    def students_to_model(self):
        students_in_activities = {}
        for day in self.schedule.days.values():
            for slot in day.slots:
                if slot.activity is not None:
                    student_set = set()
                    for student in slot.activity.students:
                        student_set.add(student)
                    students_in_activities.update({(slot.activity.course.name, slot.activity.category): student_set})

        return students_in_activities