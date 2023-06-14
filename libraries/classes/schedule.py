from libraries.helpers.load_data import load_halls
from libraries.classes.day import Day


class Schedule:
    def __init__(self, path: str = "data") -> None:
        self.days = self._init_schedule(path)

    def _init_schedule(self, path):
        halls = load_halls(path)

        # create empty timeslots for each day
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        timeslots = [str(i) for i in range(9, 17, 2)]
        days = {}
        for day in weekdays:
            # Initiate empty schedule 9:00 to 15:00.
            days.update({day: Day(day, timeslots, halls)})
        return days

    def day_schedule(self, day):
        """Return list of slot objects of a day."""
        day_list = []
        for element in self.days.items():
            if element[0] == day:
                day_list.append(element[1])
        return day_list

    def insert_activity(self, day, index, activity):
        """Try to insert activity into empty and valid slot."""
        slot = self.days[day].slots[index]
        if slot.is_empty:
            slot.fill(activity)
            return True
        return False

    def as_list_of_dicts(self):
        """Return Schedule as list of dicts for pandas dataframe."""

        return [slot.as_dict() for day in self.days.values() for slot in day.slots]

    def __repr__(self) -> str:
        """Return string representation of schedule."""
        string = ""
        for day in self.days.values():
            for slot in day.slots:
                if slot.activity is not None:
                    string = (
                        string
                        + f"day: {day.name} time: {slot.time} room: {slot.room} activity: {slot.activity.course.name}, {slot.activity.category} \n"
                    )
                else:
                    string = (
                        string
                        + f"day: {day.name} time: {slot.time} room: {slot.room} activity: None \n"
                    )
        return string
