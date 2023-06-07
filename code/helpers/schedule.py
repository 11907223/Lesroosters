from copy import deepcopy
import pandas as pd
import json


class Schedule:
    def __init__(self, df_halls) -> None:
        """Generate a schedule for all classes in roster.

        Args:
            df_halls (pd.DataFrame): Contains lecture hall information.
        """
        self.schedule = self.init_empty_schedule(df_halls)

    def init_empty_schedule(
        self, df_halls: pd.DataFrame
    ) -> dict[str, dict[str, dict[str, str]]]:
        """Initialize an empty schedule to fill in.

        Args:
            df_halls (pd.Dataframe): Contains lecture hall information.

        Returns:
            dict[str, dict[str, dict[str, dict[str, str]]]:
                Structure of days containing timeslots containing lecture halls.
                Lecture halls can have a course assigned.
        """
        weekday: list[str] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        hall_ids: list[str] = list(df_halls["Zaalnummer"])
        hallslot: dict[str, str] = {id: [] for id in hall_ids}
        timeslot: dict[str, dict[str, str]] = {
            str(i): deepcopy(hallslot) for i in range(9, 19, 2)
        }
        schedule: dict[str, dict[str, dict[str, str]]] = {
            day: deepcopy(timeslot) for day in weekday
        }
        return schedule

    def dump_courses_in_schedule(self, df_courses):
        """Dump all courses into schedule.

        This function does not take lecture hall capacity into account.
        Assigns each course the required number of halls as stated in its datafile.

         Args:
            df_courses (pd.Dataframe): Dataframe containing courses to dump.

         Returns:
            True succesful dump of courses into schedule.
            False if dump was not completed.
        """
        course_id = 0
        lecture_count: int = self.calc_total_lecture_count(df_courses.iloc[course_id])

        # Return True if the course is in the schedule.
        for day in self.schedule.values():
            # Return True if lecture count is 0 or 29
            for timeslot in day.values():
                # Add a new hall to the timeslot
                for hall in timeslot.values():
                    hall.append(df_courses.iloc[course_id]["Vak"])
                    lecture_count -= 1
                    # Check if lecture count is 0 or 29
                    if lecture_count == 0:
                        course_id += 1

                        # Return True if lecture count is valid.
                        if course_id == 29:
                            # quit condition
                            return True
                        else:
                            lecture_count = self.calc_total_lecture_count(
                                df_courses.iloc[course_id]
                            )
        return False

    def calc_total_lecture_count(self, df_course: pd.Series):
        """Calculate total lecture count for a course.

        The lecture count is the sum of Hoorcolleges, Practica and Werkcolleges.
        (Hoorcolleges = Lectures, Practica = Practicals, Werkcolleges = Tutorials)

        Args:
            df_course (pd.Series): Series containing course data.

         Returns:
            int: number of lectures in the course
        """
        return int(
            df_course["#Hoorcolleges"]
            + df_course["#Practica"]
            + df_course["#Werkcolleges"]
        )

    def add_course(
        self, day: str, timeslot: int, course: str, type: str, location: str
    ):
        """Add a course to the schedule.

        Args:
                day (str): Day to add the course to
                timeslot (int): Time - slot to add the course to
                course (str): Name of the course to add e. g.
                type (): Type of the course.
                    P(Practical), L(Lecture), T(Tutorial)
                location: Location to add the course
        """
        self.schedule[day][timeslot].update(
            {location: {"coursename": course, "type": type}}
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the schedule. This is useful for debugging purposes. The string representation can be converted to a more understandable format using the : py : func : ` str ` function.


        Returns:
                A string representation of the schedule in the format used by the : py : func : ` str ` function
        """
        return str(self.schedule)


# This function is called from the main module.
if __name__ == "__main__":
    schedule = Schedule(pd.read_csv("../../data/zalen.csv"))

    df = pd.read_csv("../../data/vakken.csv")
    schedule.dump_courses_in_schedule(df)
    print(json.dumps(schedule.schedule, indent=4))
