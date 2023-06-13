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

    def exceed_capacity(self, activity):
        """Check if nr. of students in activity smaller than room capacity.
        Returns none if room capacity is not exceded. Returns integer with
        capacity difference if capacity is exceded.
        """

        # Check if activity has smaller capacity than room
        if activity.capacity <= self.room_capacity:
            return None
        else:
            # capacity not satisfied
            return activity.capacity - self.room_capacity

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
        return f"{self.day} {self.time} {self.room}"
