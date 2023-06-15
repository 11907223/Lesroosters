from libraries.classes.hallslot import Hall_slot


class Day:
    def __init__(self, weekday: str, timeslots: list[str], halls: dict[str, int]) -> None:
        """Initialize a Day.

        Args:
                weekday (list[str]): The weekday of the instance.
                timeslots (list[str]): The timeslots of the instance.
                halls (dict[str, int]): The halls of the instance.6
        """
        self.name = weekday
        self.slots = self._init_slots(halls, timeslots)

    def _init_slots(self, halls: dict[str, int], timeslots: list[str]) -> 'list[Hall_slot]':
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
