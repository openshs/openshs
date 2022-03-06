from tkinter import *
from tkinter import messagebox
from config.config import Config
from main_ui.list_boxes import ListBoxes
from .calendar_picker import *
from .utils import *
from .aggregate_popup import *

class MenuBar:
    def __init__(self, window: Tk, custom_config: Config) :
        self.__window = window
        self.__l_boxes:ListBoxes = None
        self.__custom_config = custom_config

        verbose = BooleanVar()
        verbose.set(False)
        # Function for enabling or disabling context information in hud view
        def enableVerbose() :
            if verbose.get() == 1: self.__custom_config.setVerbose(True)
            elif verbose.get() == 0: self.__custom_config.setVerbose(False)

        darkmode = BooleanVar()
        darkmode.set(False)
        # Function for displaying UI components as dark or light
        def darkMode():
            if darkmode.get() == 1: self.__window.config(background='black')
            elif darkmode.get() == 0: self.__window.config(background='white')
            else: messagebox.showerror('Error', 'Something went wrong!')

        self.__menubar = Menu(self.__window, foreground='black', activebackground='white', activeforeground='black')  

        optionsm = Menu(self.__menubar, tearoff=0, foreground='black') 
        
        # Function for openning the simulator
        def genDatasets():
            if len(self.__l_boxes.getLEscenarios().curselection())!=0:
                # Choose date and time:
                dtPick = DateTimePicker(self.__window)
                self.__window.wait_window(dtPick)
                if not dtPick.cancel :
                    dt = dtPick.date+' '+dtPick.time
                    # Hide main window
                    self.__window.withdraw()
                    flag = startGenData(
                        self.__l_boxes.getLEscenarios().get(
                            self.__l_boxes.getLEscenarios().curselection()[0]), 
                        dt, 
                        self.__custom_config
                    )
                    if not flag: messagebox.showwarning('Wrong context', 
                        'The selected context does not refer to a blender file') 
            else: 
                messagebox.showwarning('Missing context', 
                    'A context must be chosen')
            # Update list boxes
            self.__l_boxes.update()
            # Show main window
            window.deiconify()
        optionsm.add_command(label='Generate datasets', command=genDatasets)  
        # Function for openning the simulator in interactive mode
        def interactiveMode():
            if len(self.__l_boxes.getLEscenarios().curselection())!=0:
                # Choose date and time:
                dtPick = DateTimePicker(self.__window)
                self.__window.wait_window(dtPick)
                if not dtPick.cancel :
                    dt = dtPick.date+' '+dtPick.time
                    # Hide main window
                    self.__window.withdraw()
                    flag = startIntMode(
                        self.__l_boxes.getLEscenarios().get(
                            self.__l_boxes.getLEscenarios().curselection()[0]), 
                        dt, 
                        self.__custom_config
                    )
                    if not flag: messagebox.showwarning('Wrong context', 
                        'The selected context does not refer to a blender file') 
            else: 
                messagebox.showwarning('Missing context', 
                    'A context must be chosen')
            # Update list boxes
            self.__l_boxes.update()
            # Show main window
            window.deiconify()
        optionsm.add_command(label='Interactive mode', command=interactiveMode)  
        optionsm.add_separator()
        optionsm.add_command(label="Exit", command=window.quit)  
        self.__menubar.add_cascade(label="Options", menu=optionsm)  

        toolsm = Menu(self.__menubar, tearoff=0)  
        def replicateDS():
            l_aux = []
            for i in range(self.__l_boxes.getLEscenarios().size()):
                l_aux.append(self.__l_boxes.getLEscenarios().get(i))
            print(l_aux)
            if(len(l_aux)):
                agP = AgreggatePopup(self.__window, l_aux)
                self.__window.wait_window(agP)
                # Update list boxes
                self.__l_boxes.update()
            else: 
                messagebox.showwarning('Missing contexts', 
                    'No context avilable')
        toolsm.add_command(label="Replicate datasets", command=replicateDS) 
        self.__menubar.add_cascade(label="Tools", menu=toolsm)  

        configm = Menu(self.__menubar, tearoff=0)
        configm.add_checkbutton(label='Enable verbose', onvalue=1, offvalue=0, variable=verbose, command=enableVerbose)
        self.__menubar.add_cascade(label="Config", menu=configm)

        viewm = Menu(self.__menubar, tearoff=0)
        viewm.add_checkbutton(label='Darkmode', onvalue=1, offvalue=0, variable=darkmode, command=darkMode)
        self.__menubar.add_cascade(label='View', menu=viewm)

        help = Menu(self.__menubar, tearoff=0)

        # Function for displaying info
        def about(): messagebox.showinfo('Info', '...')
        help.add_command(label="About", command=about)  
        self.__menubar.add_cascade(label="Help", menu=help)  
        
    def getMenuBar(self):
        return self.__menubar

    def setListBoxes(self, lb:ListBoxes):
        self.__l_boxes = lb