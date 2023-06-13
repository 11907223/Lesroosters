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
