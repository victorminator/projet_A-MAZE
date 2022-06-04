import PySimpleGUI as sg
from os import path

FILENAME = "-NAME-"
WIDTH = "-WIDTH-"
HEIGHT = "-HEIGHT-"
CREATE = "-CREATE-"
ERRORS = "-ERROR-"

MIN_DIM = 8
MAX_DIM = 48

def valid_dimension(dimension, min_dim=MIN_DIM, max_dim=MAX_DIM):
    try:
        entier = int(dimension)
        if entier >= min_dim and entier <= max_dim:
            return str(entier)
        return f"Error: the dimensions must be between {min_dim} and {max_dim}"
    except:
        return "Error: dimensions have to be positive integers"

def main():
    wn_layout = [
        [sg.Text("To create a level, please name it and give its dimensions")],
        [sg.Text("Filename: "), sg.Input(key=FILENAME)],
        [sg.Text("Width: "), sg.Input(key=WIDTH, size=(3, 1)), sg.Push(), sg.Button("Create", key=CREATE, size=(7, 2)), sg.Push()],
        [sg.Text("Height : "), sg.Input(key=HEIGHT, size=(3, 1))],
        [sg.Push(), sg.Text("", key=ERRORS), sg.Push()]
    ]

    create_window = sg.Window("Create level", layout=wn_layout)
    is_running = True

    while is_running:
        event, values = create_window.read()
        if event == sg.WIN_CLOSED:
            is_running = False

        if event == CREATE:
            width, height = map(valid_dimension, (values[WIDTH], values[HEIGHT]))
            if not width.isdigit():
                create_window[ERRORS].update(width)
            elif not height.isdigit():
                create_window[ERRORS].update(height)
            elif path.exists(values[FILENAME] + ".mznv"):
                create_window[ERRORS].update("Error: filename already exists!")
            else:
                fic = open(values[FILENAME] + ".mznv", mode="w")
                fic.write(f"{width} {height}")
                fic.close()
                create_window.close()
                return values[FILENAME] + ".mznv"
    create_window.close()
    return False