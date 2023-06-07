import PySimpleGUI as sg
import pandas as pd


def display_schedule(df):
    # Define the row headers as a list
    row_headers = [
        "09:00-11:00",
        "11:00-13:00",
        "13:00-15:00",
        "15:00-17:00",
        "17:00-19:00",
    ]

    # Insert the row headers as a new column
    df.insert(0, "Timeslot", row_headers)

    # Display lecture halls and course names as values
    a1_04 = df["Monday"]["9"]

    print(a1_04)
    # Create the GUI layout
    layout = [
        [sg.Text("Schedule")],
        [
            sg.Table(
                values=df.values.tolist(),
                headings=df.columns.tolist(),
                display_row_numbers=False,
                font=("Arial", 12),
                justification="left",
                auto_size_columns=False,
                row_height=45,
                num_rows=len(df),
                col_widths=[10] + [40] * (len(df.columns) - 1),
            )
        ],  # Add the DataFrame as a table
        [sg.Button("CLOSE")],
    ]

    # Create the window
    window = sg.Window("Schedule", layout, size=(900, 600))

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the CLOSE button
        if event == "CLOSE" or event == sg.WIN_CLOSED:
            break

    window.close()

    return None
