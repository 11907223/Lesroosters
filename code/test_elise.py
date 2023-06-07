import pandas as pd
import sys

sys.path.append("./helpers/")
from schedule import scheduler


df_vakken = pd.read_csv("../data/vakken.csv")
df_zalen = pd.read_csv("../data/zalen.csv")

schedule = scheduler()

print(
    df_vakken.iloc[0]["Vak"],
    df_vakken.iloc[0]["#Hoorcolleges"]
    + df_vakken.iloc[0]["#Practica"]
    + df_vakken.iloc[0]["#Werkcolleges"],
)

for expected in df_vakken["Verwacht"]:
    bob = [
        df_zalen[df_zalen["Max. capaciteit"] == i].sort_values(
            "Max. capaciteit", ascending=True
        )
        for i in df_zalen["Max. capaciteit"]
        if i >= expected
    ]
    print(bob)

schedule = scheduler()
vak_id = 0
n_colleges: int = (
    df_vakken.iloc[vak_id]["#Hoorcolleges"]
    + df_vakken.iloc[vak_id]["#Practica"]
    + df_vakken.iloc[vak_id]["#Werkcolleges"]
)

while vak_id < len(df_vakken):
    for day in schedule.values():
        for timeslot in day.values():
            for hall in timeslot.values():
                if vak_id == 29:
                    break
                hall.update({df_vakken.iloc[vak_id]["Vak"]: n_colleges})
                n_colleges -= 1
                if n_colleges == 0:
                    vak_id += 1
                    if vak_id < 29:
                        n_colleges: int = (
                            df_vakken.iloc[vak_id]["#Hoorcolleges"]
                            + df_vakken.iloc[vak_id]["#Practica"]
                            + df_vakken.iloc[vak_id]["#Werkcolleges"]
                        )

print(schedule)
