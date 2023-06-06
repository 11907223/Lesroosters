import pandas as pd


def scheduler():
    weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    timeslot = [f"{i}:00 - {i + 2}:00" for i in range(9, 19, 2)]
    df = pd.DataFrame(index=timeslot, columns=weekday)
    building_schedule = {i: df for i in range(7)}
    return building_schedule
