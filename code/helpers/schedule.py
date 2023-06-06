import copy


def scheduler():
    weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    timeslot = {i: {} for i in range(9, 19, 2)}
    schedule = {}
    for day in weekday:
        schedule[day] = copy.deepcopy(timeslot)
    return schedule


class Schedule:
    def __init__(self) -> None:
        self.schedule: dict[any] = scheduler()

    def add_course(self, day: str, timeslot: int, course: str, type: str, location: str):
        """
        
        Args:
            day (str): Day.
            timeslot (str): sada
            course (str):

        """
        self.schedule[day][timeslot].update({location: {"coursename": course, "type": type}})

s = Schedule()
s.add_course("Monday", 9, "Statistics", "werkcollege", "hier")
s.add_course("Friday", 11, "Ananas", "diner", "daar")
s.add_course("Monday", 9, "Patat", "ontbijt", "daar")
print(s.schedule)