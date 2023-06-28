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

    # Create a list of weekdays (column headers)
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # Create a list of timeslots (row headers)
    timeslots = ["9-11", "11-13", "13-15", "15-17", "17-19"]

    # Create an empty DataFrame
    df = pd.DataFrame(index=timeslots, columns=weekdays)

    # Iterate over the dictionary and populate the DataFrame
    for index, (course, lecture) in schedule.items():
        if course is not None and lecture is not None:
            day = index // 29
            timeslot_index = (index % 29) // 7

            # Map the timeslot index to the corresponding timeslot
            timeslot = timeslots[timeslot_index]

            # Map the location to the corresponding weekday
            weekday = weekdays[day]

            # Check if the cell is already populated
            if pd.notnull(df.loc[timeslot, weekday]):
                # Concatenate the new value with the existing value
                existing_value = df.loc[timeslot, weekday]
                new_value = f"{existing_value}\n{course}, {lecture}"
                df.loc[timeslot, weekday] = new_value
            else:
                # Assign the value to the cell
                df.loc[timeslot, weekday] = f"{course}, {lecture}"

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
        rowheight=120,
        fieldbackground="#677a46",
        font=("Arial", 12),
        wraplength=50,
    )

    # Create a Treeview widget
    tree = ttk.Treeview(window, style="Custom.Treeview")
    tree["columns"] = [""] + df.columns.tolist()
    tree["show"] = "headings"

    # Add rows to the Treeview
    tree.insert(
        "",
        tk.END,
        values=[""] + df.columns.tolist(),
        tags="header",
    )  # Column headers row
    for index, row in df.iterrows():
        tree.insert("", tk.END, values=[index] + row.tolist())

    # Define a function to apply cell colors based on conditions
    # def apply_cell_colors():
    #     for i, col in enumerate(df.columns):
    #         for j, value in enumerate(df[col]):
    #             if pd.isnull(value):  # Check for None or NaN values
    #                 continue  # Skip empty cells
    #             elif value == "Some Condition":
    #                 tree.tag_configure(f"cell_{i}_{j}", background="red")
    #             elif value == "Another Condition":
    #                 tree.tag_configure(f"cell_{i}_{j}", background="blue")
    #             # Add more conditions and colors as needed

    # # Call the function to apply cell colors
    # apply_cell_colors()

    # # Apply the cell colors to the Treeview
    # for i, col in enumerate(df.columns):
    #     for j, value in enumerate(df[col]):
    #         if pd.isnull(value):  # Check for None or NaN values
    #             continue  # Skip empty cells
    #         tree.item(f"::I{j}::T{i}", tags=f"cell_{i}_{j}")

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
