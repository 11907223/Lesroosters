import PySimpleGUI as sg


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

    # value = df["Monday"]["9"]["A1.04"]

    for hall in df["Monday"]["9"]:
        print(df["Monday"]["9"][hall])
        print(hall)

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
                auto_size_columns=True,
                row_height=100,
                num_rows=len(df),
                key="-TABLE-",
                expand_x=True,
                expand_y=True,
            )
        ],  # Add the DataFrame as a table
        [sg.Button("CLOSE")],
    ]

    # Create the window
    window = sg.Window("Schedule", layout, size=(1000, 700))

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the CLOSE button
        if event == "CLOSE" or event == sg.WIN_CLOSED:
            break

    window.close()

    return None
