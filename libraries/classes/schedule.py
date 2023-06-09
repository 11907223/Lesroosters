import csv
from libraries.helpers.load_data import load_halls


class ScheduleSlot:
    def __init__(self, day, time, room, room_capacity, activity=None) -> None:
        self.day = day
        self.time = time
        self.room = room
        self.room_capacity = room_capacity
        self.activity = activity

    def is_empty(self) -> bool:
        """Check if slot is empty."""
        if not self.activity:
            return True
        else:
            return False

    def fill(self, activity) -> None:
        """Fill the slot with an activity."""
        self.activity = activity

    def check_capacity(self, activity):
        """Check if nr. of students in activity smaller than room capacity."""
        if self.room_capacity >= activity.capacity:
            return True

        # capacity not satisfied
        return False

    def as_dict(self):
        """Return ScheduleSlot object as a dict (for pandas dataframes)."""

        if self.activity:
            return {
                "day": self.day,
                "time": self.time,
                "room": self.room,
                "course": self.activity.course,
                "activity": self.activity.category,
            }
        return {
            "day": self.day,
            "time": self.time,
            "room": self.room,
            "course": None,
            "activity": None,
        }

    def __repr__(self) -> str:
        """Return string representation of this ScheduleSlot object."""

        return f"{self.day} starting at {self.time} in room {self.room}"


class Schedule:
    def __init__(self, path: str="data") -> None:
        self.slots = self._init_schedule(path)

    def _init_schedule(self, path):
        halls = load_halls(path)

        # create all empty timeslots
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        timeslots = [str(i) for i in range(9, 19, 2)]
        slots = []
        for day in weekdays:
            for timeslot in timeslots:
                for hall_id, capacity in halls.items():
                    slots.append(ScheduleSlot(day, timeslot, hall_id, capacity))

        return slots

    def day_schedule(self, day):
        """Return list of slot objects of a day."""
        day_list = []
        for slot in self.slots:
            if slot.day == day:
                day_list.append(slot)
        return day_list

    def insert_activity(self, activity, random=True):
        """Insert activity into empty and valid slot."""
        if random:
            # insert activity in random slot
            while True:
                index = random()*(len(self.slots)-1)
                slot = self.slots[index]
                if slot.is_empty() and slot.check_capacity(activity):
                    slot.fill(activity)
                    return True
        else:
            # just insert into next empty and valid slot
            for slot in self.slots:
                if slot.is_empty() and slot.check_capacity(activity):
                    slot.fill(activity)
                    return True
            return False

    def as_list_of_dicts(self):
        """Return Schedule as list of dicts for pandas dataframe."""

        return [slot.as_dict() for slot in self.slots]

    def __repr__(self) -> str:
        """'Return string representation of schedule."""
        string = ""
        for slot in self.slots:
            if slot.activity:
                string = (
                    string
                    + f"day: {slot.day} time: {slot.time} room: {slot.room} activity: {slot.activity.course}, {slot.activity.category} \n"
                )
            else:
                string = (
                    string
                    + f"day: {slot.day} time: {slot.time} room: {slot.room} activity: None \n"
                )
        return string
