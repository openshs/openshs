import PySimpleGUI as sg
import os.path

menu_def = [
    ['Options', ['Generate datasets', 'Tests IA']],
    ['Tools', ['Replicate datasets', 'Train IA'],],
    ['Config', ['Enable verbose'],],
    ['Help', 'About...']
]
                
scenarios = [
    'morning',
    'afernoon',
    'evening',
    'test1'
]
datasets = [
    'weekday_morning',
    'weekday_afernoon',
    'weekday_evening',
    'weekday_test1'
]
ia_mech = [
    'Lights disable',
    'Wheater predictor',
    '...',
    '...'
]

layout = [
    [sg.Menu(menu_def)],
    [
        sg.Text('Scenarios:'),
        sg.Text('\t\t\tDatasets:'),
        sg.Text('\t\t\tIA Mechanisms:')
    ],
    [
        sg.Listbox(scenarios, size=(30, 20)),
        sg.Listbox(datasets, size=(30, 20)),
        sg.Listbox(ia_mech, size=(30, 20))
    ]
]

window = sg.Window("OpenSHS", layout)

# Event loop:
while True:
    event, values = window.read()
    # End program if button is pressed
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()