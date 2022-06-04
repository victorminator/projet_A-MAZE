import PySimpleGUI as sg
from os import path


def main():
    OPENED_FILE = "-FPATH-"
    BROWSE_FILE = "-BFILE-"
    SUBMIT_INFO = "-SUB-"
    ERRORS_TEXT = "-ERROR-"

    layout = [
        [sg.Text("To open and edit an existing level, please give the path leading to the file")],
        [sg.Input(key=OPENED_FILE, expand_x=True), sg.Button("Browse", key=BROWSE_FILE)],
        [sg.Push(), sg.Button("Open", key=SUBMIT_INFO), sg.Push()],
        [sg.Push(), sg.Text(key=ERRORS_TEXT), sg.Push()]
    ]

    edit_window = sg.Window("Open file", layout=layout)
    is_run = True

    while is_run:
        event, values = edit_window.read()

        if event == sg.WIN_CLOSED:
            is_run = False
        
        if event == BROWSE_FILE:
            path_name = sg.filedialog.askopenfilename()
            if path_name:
                edit_window[OPENED_FILE].update(path_name)
        
        if event == SUBMIT_INFO:
            nom_fic = values[OPENED_FILE]
            if not path.exists(nom_fic):
                edit_window[ERRORS_TEXT].update("Error: path does not exist")
            elif nom_fic[len(nom_fic) - 4:] != "mznv":
                edit_window[ERRORS_TEXT].update("Error: please open a .mznv file")
            else:   
                edit_window.close()
                return values[OPENED_FILE]
    edit_window.close()
    return False