from libraries.classes.schedule import Schedule
from libraries.classes.student import Student
from libraries.classes.course import Course


class Model:
    def __init__(
        self,
        courses: dict[str, Course],
        students: dict[str, Student],
        schedule: Schedule,
    ) -> None:
        self.courses = courses
        self.students = students
        self.schedule = schedule
        self.model = self.get_empty_model()
        self.activities = self.empty_student_model()
        self.index_penalties = {}  # empty model {index: penalty}
        self.student_penalties = (
            {}
        )  # empty activities model with {activity: {student_id: penalty}}

    def get_empty_model(self) -> str:
        """Takes Schedule object and flattens it into string representation.
        string looks like:

        """
        schedule_model = {}

        for index, entry in enumerate(self.schedule.as_list_of_dicts()):
            day = entry["day"]
            local_index = index % 29
            activity = entry["activity"]
            course = entry["course"]

            if day not in schedule_model:
                schedule_model[day] = {}

            if "index" not in schedule_model[day]:
                schedule_model[day]["index"] = {}

            schedule_model[day]["index"][local_index] = {
                "course": course,
                "activity": activity,
            }

        return schedule_model

    def empty_student_model(self) -> str:
        """Flattens Students and Activity objects into strings:
        example:

        """
        students_in_activities = {}
        for day in self.schedule.days.values():
            for slot in day.slots:
                if slot.activity is not None:
                    student_set = set()
                    for student in slot.activity.students:
                        student_set.add(student)
                    students_in_activities.update(
                        {
                            (
                                slot.activity.course.name,
                                slot.activity.category,
                            ): student_set
                        }
                    )

        return students_in_activities

    def return_models(self):
        """Returns schedule and activities-student strings"""
        return self.model, self.activities

    def add_activity(self, activity: tuple[str, str], index: int) -> bool:
        """adds activity to given index in schedule model"""
        pass

    def remove_activity(self, activity: tuple[str, str], index: int) -> bool:
        """removes activity to given index in schedule model"""
        pass

    def get_capacity(self, index: int) -> int:
        """Returns capacity of index (hall)"""
        pass

    def get_index(self, activity: tuple[str, str]) -> int:
        """get model index of activity"""
        pass

    def add_student(self, student: int, activity: tuple[str, str]) -> bool:
        """Add student to student-activity model"""
        pass

    def remove_student(self, student: int, activity: tuple[str, str]) -> bool:
        """remove student to student-activity model"""
        pass

    def student_activities(self, student: int) -> list[int]:
        """Returns list of indexes of activities"""
        pass

    def get_highest_n_penalties(self, n) -> list[list[tuple[str, str], int]]:
        """Searches the schedule for activities with highest penalties.
        Returns a list of length n where each element represents an activity that
        caused a high penalty, this element is a list which contains a tuple with course name
        and activity type, the day, and the index. The first element (list[0])
        is the activty with the highest penalty and the last element (list[n]) is the
        activity with the lowest penalty.

        list[list[activity: tuple[str, str], index: int]]"""
        pass

    # def get_highest_n_students(self, n) -> list[list[int, tuple[str, str]]]:
    #     """Searches the model for students in activities with highest penalties.
    #     Returns a list of length n where each element represents a student that
    #     caused a high penalty, this element is a list which contains a tuple with course name
    #     and activity type, the day, and the index. The first element (list[0])
    #     is the activty with the highest penalty and the last element (list[n]) is the
    #     activity with the lowest penalty.

    #     list[list[student: int, activity: tuple[str, str]]"""
    #     pass

    def capacity_penalty(self) -> int:
        """Calculate penalties of activities and hall capacity.
        Fills in empty model with {index: penalty}.
        Returns total capacity penalty."""
        pass

    def evening_penalty(self) -> int:
        """Calculate penalties of activities in evening slot.
        Fills in empty model with {index: penalty}.
        returns total evening penalty."""
        pass

    def conflict_penalty(self) -> int:
        """Calculates penalties of students with course conflicts.
        Fills in empty student activity model {activity: {student_id: penalty}}.
        returns total conflict penalty."""
        pass

    def total_penalty(self) -> int:
        total = (
            self.capacity_penalty() + self.evening_penalty() + self.conflict_penalty()
        )
        return total
