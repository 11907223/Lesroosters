from libraries.helpers.load_data import load_halls
import pandas as pd
import tkinter as tk
from tkinter import ttk


def create_df(schedule: dict) -> pd.DataFrame:
    """Takes a schedule dictionary and converts it to a pandas dataframe.

    Args:
        schedule (dict): A schedule dictionary with indices 0-144 mapping to activity tuples or None.

    Return:
        pd.DataFrame: A dataframe with weekdays as column headers, timeslots as row headers and activities
            filled in the schedule on the correct day and timeslot.
    """

    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    timeslots = ["9-11", "11-13", "13-15", "15-17", "17-19"]
    halls = load_halls()

    # Create an empty DataFrame
    df = pd.DataFrame(index=timeslots, columns=weekdays)

    # Iterate over the dictionary and populate the DataFrame
    for index, (course, lecture) in schedule.items():
        if course is not None and lecture is not None:
            day = index // 29
            timeslot_index = (index % 29) // 7
            if (index % 29) == 28:
                # Evening slot exception.
                hall = 5
            else:
                # Regular hall indexing.
                hall = (index % 29) % 7

            # Map the timeslot index to the corresponding timeslot
            timeslot = timeslots[timeslot_index]

            # Map the location to the corresponding weekday
            weekday = weekdays[day]

            value = f"{course}\n- {lecture}, {halls[hall]}"

            # Check if the cell is already populated
            if pd.notnull(df.loc[timeslot, weekday]):
                # Concatenate the new value with the existing value
                existing_value = df.loc[timeslot, weekday]
                new_value = f"{existing_value}\n{value}"
                df.loc[timeslot, weekday] = new_value
            else:
                # Assign the value to the cell
                df.loc[timeslot, weekday] = value

    return df


def tkinter_pop_up(df: pd.DataFrame) -> None:
    """Function to create a pop up window that shows a schedule with tkinter.

    Args:
        df (pd.Dataframe): A schedule dataframe with column header weekdays and row header timeslots.
    """

    # Create a Tkinter window
    window = tk.Tk()
    window.title("Schedule Viewer")

    # Configure a custom style for the table
    style = ttk.Style()
    style.configure(
        "Custom.Treeview",
        background="#FFFFE0",
        foreground="black",
        rowheight=150,
        fieldbackground="#677a46",
        font=("Arial", 12),
        wraplength=50,
    )

    # Create a Treeview widget
    tree = ttk.Treeview(window, style="Custom.Treeview")
    tree["columns"] = [""] + df.columns.tolist()
    tree["show"] = "headings"

    # Add column headings to the Treeview
    for col in df.columns:
        tree.heading(col, text=col)

    # Add rows to the Treeview
    for index, row in df.iterrows():
        tree.insert("", tk.END, values=[index] + row.tolist())

    # Add Treeview to a scrollable frame
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(expand=True, fill=tk.BOTH)

    # Start the Tkinter event loop
    window.mainloop()


def visualize_schedule(schedule: dict) -> None:
    """Visualizes a schedule in a pop up window.

    Args:
        schedule (dict): A schedule dictionary with indices 0-144 that map to activity tuples.
    """

    df = create_df(schedule)
    tkinter_pop_up(df)
