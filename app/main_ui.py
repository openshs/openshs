import PySimpleGUI as sg
import os.path

# Layout of two columns
first_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse()
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20),
            key="-FILE LIST-"
        )
    ]
]

# Show the name of the selected file
second_column = [
    [sg.Text("Choose an image from the list on the left")],
    [sg.Text(size=(40,1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")]
]

layout = [
    [
        sg.Column(first_column),
        sg.VSeparator(),
        sg.Column(second_column)
    ]
]

window = sg.Window("Image Viewer", layout)

# Event loop:
while True:
    event, values = window.read()
    # End program if button is pressed
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith( (".png", ".gif") )
        ]
        window["-FILE LIST-"].update(fnames)
    # File was chosen
    elif event == "-FILE LIST-": 
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window("-IMAGE-").update(filename=filename)
        except:
            pass

window.close()