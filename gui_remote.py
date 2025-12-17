import tkinter as tk

# -------- Command definitions --------
COMMANDS = {
    0: "1",
    1: "2",
    2: "3",
    3: "4",
    4: "5",
    5: "6",
    6: "7",
    7: "8",
    8: "9",
    9: "0",
    10: "CH+",
    11: "CH-",
    12: "VOL+",
    13: "VOL-",
    14: "MUTE",
    15: "POWER",
    16: "LAST",
    17: "UNUSED",
    18: "TV / AV",
    19: "SLEEP",
    20: "MENU",
    21: "NAV UP",
    22: "NAV DOWN",
}

# -------- Functions triggered by button events --------
def on_button_press(command_number):
    print(f"Pressed: {command_number} ({COMMANDS[command_number]})")
    # TODO: start action (e.g. send command, begin repeat)

def on_button_release(command_number):
    print(f"Released: {command_number} ({COMMANDS[command_number]})")
    # TODO: stop action (e.g. stop repeat, cleanup)

# -------- GUI setup --------
root = tk.Tk()
root.title("Remote Control")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# -------- Create buttons --------
row = 0
col = 0

for cmd_num, label in COMMANDS.items():
    btn = tk.Button(
        frame,
        text=label,
        width=10,
        height=2
    )

    # Bind press & release events
    btn.bind(
        "<ButtonPress-1>",
        lambda e, c=cmd_num: on_button_press(c)
    )
    btn.bind(
        "<ButtonRelease-1>",
        lambda e, c=cmd_num: on_button_release(c)
    )

    btn.grid(row=row, column=col, padx=5, pady=5)

    col += 1
    if col >= 4:  # buttons per row
        col = 0
        row += 1

root.mainloop()
