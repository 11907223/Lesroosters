class Penalty:
    """Class to calculate the penalty points of a Schedule object."""

    def __init__(self, schedule) -> None:
        self.schedule = schedule

    def total_penalty(self) -> int:
        """Total number of penalty points for a week schedule."""
        total = (
            self.capacity_penalty() + self.evening_penalty() + self.student_penalty()
        )
        return total

    def capacity_penalty(self) -> int:
        """Check if the number of students of each activity exceeds the hall capacity.
        For every student that doesn't fit 1 penalty point is counted."""
        penalty_points = 0
        day_schedules = self.schedule.days.values()

        for day in day_schedules:
            for slot in day.slots:
                if slot.activity:
                    if not slot.check_capacity(slot.activity):
                        penalty_points += 1

        return penalty_points

    def student_penalty(self) -> int:
        """Every course conflict (more than 1 activity in timeslot) for a student
        schedule is counted as 1 penalty point."""
        penalty_points = 0

        return penalty_points

    def evening_penalty(self) -> int:
        """If the evening timeslot (17:00-19:00) is used, a penalty of 5 points is counted."""
        penalty_points = 0

        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            day_schedule = self.schedule.day_schedule(day)
            if day_schedule[0].slots[-1].activity:
                penalty_points += 5

        return penalty_points

    def empty_timeslot(self) -> int:
        penalty_points = 0

        for day in self.schedule.days.values():
            students_in_day = []
            for slot in day:
                students_in_day.append(slot.activity.students)
            