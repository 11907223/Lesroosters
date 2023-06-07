import copy
from collections import defaultdict


def scheduler():
    weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    hall_ids = ["A1.04", "A1.06", "A1.08", "A1.10", "B0.201", "C0.110", "C1.112"]
    hallslot = {id: {} for id in hall_ids}
    timeslot = {str(i): copy.deepcopy(hallslot) for i in range(9, 19, 2)}
    schedule = {day: copy.deepcopy(timeslot) for day in weekday}
    return schedule


class Schedule:
    def __init__(self) -> None:
        self.schedule = scheduler()

    def find_next_empty_slot(self):
        pass

    def add_course(
        self, day: str, timeslot: int, course: str, type: str, location: str
    ):
        """

        Args:
            day (str): Day.
            timeslot (str): sada
            course (str):

        """
        self.schedule[day][timeslot].update(
            {location: {"coursename": course, "type": type}}
        )
