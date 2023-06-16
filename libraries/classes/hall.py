class Hall:
    def __init__(self, name, capacity) -> None:
        self.name: str = name
        self.capacity: int = capacity

    def __repr__(self) -> str:
        """Return string representation of this ScheduleSlot object."""
        return f"{self.name}"
