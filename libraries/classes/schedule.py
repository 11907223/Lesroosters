from libraries.helpers.load_data import load_halls


class Hall_slot:
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

    def get_activity_exceeding_capacity(self, activity):
        pass

    def as_dict(self):
        """Return ScheduleSlot object as a dict (for pandas dataframes)."""

        if self.activity:
            return {
                "day": self.day,
                "time": self.time,
                "room": self.room,
                "course": self.activity.course.name,
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


class Day:
    def __init__(self, weekday: str, timeslots, halls) -> None:
        """Initialize a Day.

        Args:
            weekday (list[str]): The weekday of the instance.
            timeslots (list[str]): The timeslots of the instance.
            halls (dict[str, int]): The halls of the instance.
        """
        self.name = weekday
        self.slots = self._init_slots(halls, timeslots)

    def _init_slots(self, halls, timeslots) -> list[Hall_slot]:
        """
        Initialize hall slots for this job. This is a helper method to initialize the timeslots and halls for this job.

        Args:
            halls: Dictionary of halls keyed by timeslot id.
            timeslots: List of timeslot objects. Each timeslot is represented as a dictionary with keys corresponding to the timeslot id and values corresponding to the capacity

        Returns:
            List of Hall_slot objects that have been
        """
        slots = []
        # Initiate empty schedule from 9:00 to 15:00.
        for timeslot in timeslots:
            for hall_id, capacity in halls.items():
                slots.append(Hall_slot(self.name, timeslot, hall_id, capacity))

        # Add 17:00 timeslot.
        largest_hall = list(halls)[5]
        slots.append(Hall_slot(self.name, str(17), largest_hall, halls[largest_hall]))

        return slots

    def get_penalty_points(self) -> int:
        pass
        penalty_points = 0
        for slot in self.slots:
            slot.get_


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
        for slot in self.days:
            if slot.day == day:
                day_list.append(slot)
        return day_list

    def insert_activity(self, day, index, activity):
        """Try to insert activity into empty and valid slot."""
        slot = self.days[day].slots[index]
        if slot.is_empty and slot.check_capacity(activity):
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
