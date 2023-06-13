class Penalty:
    """Class to calculate the penalty points of a Schedule object."""

    def __init__(self, schedule) -> None:
        self.schedule = schedule

    def total(self) -> int:
        """Total number of penalty points for a week schedule."""
        total = self.capacity() + self.evening() + self.course_conflict()
        return total

    def capacity(self) -> int:
        """Check if the number of students of each activity exceeds the hall capacity.
        For every student that doesn't fit 1 penalty point is counted."""

        # Start counting at 0 penalty points
        penalty_points = 0
        # Select all the Day objects in the schedule
        day_schedules = self.schedule.days.values()

        # Iterate over the Day objects
        for day in day_schedules:
            # Iterate over timeslots in day
            for slot in day.slots:
                # If slot is filled with activity
                if slot.activity:
                    # Check if capacity is exceded
                    if slot.exceed_capacity(slot.activity):
                        # Add 1 penalty point
                        penalty_points += slot.exceed_capacity(slot.activity)

        return penalty_points

    def course_conflict(self) -> int:
        """Every course conflict (more than 1 activity in timeslot) for a student
        schedule is counted as 1 penalty point."""
        penalty_points = 0
        days = self.schedule.days.values()
        students = []

        for day in days:
            for slot in day.slots:
                if slot.activity:
                    for object in slot.activity.students.values():
                        students.append(object)

        for student in students:
            print(student.activity)

        return penalty_points

    def evening(self) -> int:
        """If the evening timeslot (17:00-19:00) is used, a penalty of 5 points is counted."""

        # Start counting at 0 penalty points
        penalty_points = 0

        # Iterate over days in the week
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            # Select the Day object in the schedule
            day_schedule = self.schedule.day_schedule(day)
            # Check if there is an activity in the evening slot
            if day_schedule[0].slots[-1].activity:
                # Add 5 points if slot is filled
                penalty_points += 5

        return penalty_points

    def empty_timeslot(self) -> int:
        penalty_points = 0

        for day in self.schedule.days.values():
            students_in_day = []
            for slot in day:
                students_in_day.append(slot.activity.students)
