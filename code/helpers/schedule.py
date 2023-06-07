import copy


def init_empty_schedule():
    weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    hall_ids = ["A1.04", "A1.06", "A1.08", "A1.10", "B0.201", "C0.110", "C1.112"]
    hallslot = {id: {} for id in hall_ids}
    timeslot = {str(i): copy.deepcopy(hallslot) for i in range(9, 19, 2)}
    schedule = {day: copy.deepcopy(timeslot) for day in weekday}
    return schedule


class Schedule:
    def __init__(self) -> None:
        self.schedule = init_empty_schedule()

    def find_next_empty_slot(self):
        pass

    def add_course(
        self, day: str, timeslot: int, course: str, type: str, location: str
    ):
        """
        Args:
            day (str): Day.
            timeslot (str): sada
            course (str):
        """
        self.schedule[day][timeslot].update(
            {location: {"coursename": course, "type": type}}
        )


def fill_prototype_schedule(df_vakken):
    # empty schedule
    schedule = init_empty_schedule()

    # initial values
    vak_id = 0
    n_colleges: int = (
        df_vakken.iloc[vak_id]["#Hoorcolleges"]
        + df_vakken.iloc[vak_id]["#Practica"]
        + df_vakken.iloc[vak_id]["#Werkcolleges"]
    )

    # loop over days
    for day in schedule.values():
        # loop over timeslots
        for timeslot in day.values():
            # loop over rooms
            for hall in timeslot.values():
                # insert course
                hall.update({df_vakken.iloc[vak_id]["Vak"]: n_colleges})
                n_colleges -= 1

                # move on to next course
                if n_colleges == 0:
                    vak_id += 1

                    # quit condition
                    if vak_id == 29:
                        return schedule

                    n_colleges: int = (
                        df_vakken.iloc[vak_id]["#Hoorcolleges"]
                        + df_vakken.iloc[vak_id]["#Practica"]
                        + df_vakken.iloc[vak_id]["#Werkcolleges"]
                    )
