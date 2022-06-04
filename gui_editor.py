import PySimpleGUI as sg
import createfile
import openfile


def configuration_interface():
    CREATE_FILE = "-CRT-"
    OPEN_FILE = "-OPN-"

    popup_layout = [
        [sg.Text("Edit an existing level"), sg.Button(visible=False), sg.Button(button_text="Open File", key=OPEN_FILE, border_width=2)],
        [sg.Push(), sg.Text("OR"), sg.Push()],
        [sg.Text("Create a new level"), sg.Button("New File", key=CREATE_FILE, border_width=2)]
    ]

    fenetre = sg.Window("A-MAZE Editor", layout=popup_layout)
    app_is_running = True

    while app_is_running:
        event, _ = fenetre.read()
        
        if event == sg.WIN_CLOSED:
            app_is_running = False
        
        if event == OPEN_FILE:
            fenetre.close()
            full_path = openfile.main()
            if full_path: return full_path
        
        if event == CREATE_FILE:
            fenetre.close()
            full_path = createfile.main()
            if full_path: return full_path 
    fenetre.close()
    return -1