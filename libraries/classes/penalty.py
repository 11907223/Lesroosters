from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from libraries.classes.student import Student


class Penalty:
    """Class to calculate the penalty points of a Schedule object."""

    def __init__(self, schedule) -> None:
        self.schedule = schedule

    def total(self) -> int:
        """Total number of penalty points for a week schedule."""
        total = (
            self.capacity()
            + self.evening()
            + self.course_conflict()
            + self.empty_timeslot()
        )
        return int(total)

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

        # Start with 0 penalty points
        penalty_points = 0
        # Select all the Day objects from Schedule
        days = self.schedule.days.values()
        # Temporary variables to store students and timeslot
        temp_students: dict[int, Student] = {}
        prev_slot_time = 0

        # Iterate over Day objects
        for day in days:
            # Iterate over Hallslot objects
            for slot in day.slots:
                # If slot contains an activity at a new time
                if slot.activity and slot.time != prev_slot_time:
                    # Empty temp_students
                    temp_students = {}
                    # Set previous time to time of slot
                    prev_slot_time = slot.time
                    # Iterate over students assigned to Activity
                    for student in slot.activity.students.items():
                        # Add students to temp_students
                        temp_students.update({student[0]: student[1]})

                # If slot contains activity at same time as previous slot
                elif slot.activity and slot.time == prev_slot_time:
                    # Iterate over students assigned to Activity
                    for student in slot.activity.students.items():
                        # If student is already in temp_students
                        if student[0] in temp_students:
                            # add penalty point
                            penalty_points += 1
                        # if student not in temp_students
                        else:
                            # add student to temp_students
                            temp_students.update({student[0]: student[1]})

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

        # for day in self.schedule.days.values():
        #     students_in_day = []
        #     for slot in day:
        #         students_in_day.append(slot.activity.students)

        return penalty_points
