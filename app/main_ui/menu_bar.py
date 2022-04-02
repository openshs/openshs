from tkinter import *
from tkinter import messagebox
from config.config import Config
from config.translations import Translations
from main_ui.list_boxes import ListBoxes
from .calendar_picker import *
from .utils import *
from .aggregate_popup import *

class MenuBar:
    def __init__(self, window: Tk, custom_config: Config, translations: Translations) :
        self.__window = window
        self.__l_boxes:ListBoxes = None
        self.__custom_config = custom_config
        self.__translations = translations
        self.__menubar = Menu(self.__window, foreground='black', activebackground='white', 
            activeforeground='black')  
        self.load_menu()

    def load_menu(self):
        verbose = BooleanVar(value=False)
        # Function for enabling or disabling context information in hud view
        def enableVerbose() :
            self.__custom_config.setVerbose(bool(verbose.get()))

        def wrong_context1():
            messagebox.showwarning(
                self.get_translation('WrCont'), 
                self.get_translation('WrContInfo1')
            ) 
        def wrong_context2():
            messagebox.showwarning(
                self.get_translation('WrCont'), 
                self.get_translation('WrContInfo2')
            ) 
        def miss_context1():
            messagebox.showwarning(
                self.get_translation('MissCont'), 
                self.get_translation('MissContInfo1')
            )
        def miss_context2():
            messagebox.showwarning(
                self.get_translation('MissCont'), 
                self.get_translation('MissContInfo2')
            )
        
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
                        dt, self.__custom_config
                    )
                    if not flag: wrong_context1()
            else: miss_context1()
                
            # Update list boxes
            self.__l_boxes.update()
            # Show main window
            self.__window.deiconify()
        
        optionsm = Menu(self.__menubar, tearoff=0, foreground='black') 
        
        optionsm.add_command(label=self.get_translation('DataGen'), 
            command=genDatasets)  
        # Function for openning the simulator in interactive mode
        def interactiveMode():
            if len(self.__l_boxes.getLEscenarios().curselection())!=0:
                selection = self.__l_boxes.getLEscenarios().get(
                            self.__l_boxes.getLEscenarios().curselection()[0])
                if selection in self.__custom_config.getInteractive():
                    # Hide main window
                    self.__window.withdraw()
                    flag = startIntMode(selection, self.__custom_config)
                    if not flag: wrong_context1()
                else: wrong_context2()
            else: miss_context1()
            # Update list boxes
            self.__l_boxes.update()
            # Show main window
            self.__window.deiconify()
        optionsm.add_command(label=self.get_translation('IntMode'), 
            command=interactiveMode)  
        optionsm.add_separator()
        optionsm.add_command(label=self.get_translation('Exit'), 
            command=self.__window.quit)  
        self.__menubar.add_cascade(label=self.get_translation('Simulation'), 
            menu=optionsm)  
        
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
            else: miss_context2()
        toolsm.add_command(label=self.get_translation('RepData'), 
            command=replicateDS) 
        self.__menubar.add_cascade(label=self.get_translation('Tools'), 
            menu=toolsm)  

        configm = Menu(self.__menubar, tearoff=0)
        configm.add_checkbutton(label=self.get_translation('EnVerb'), 
            onvalue=1, offvalue=0, variable=verbose, command=enableVerbose)
        self.__menubar.add_cascade(label=self.get_translation('Config'), 
            menu=configm)

        lang_men = Menu(self.__menubar, tearoff=0)
        # Function for displaying info
        def change_lang_to_es(): 
            self.__custom_config.setLanguage('es')
            self.__custom_config.save()
            self.reload()
        def change_lang_to_en(): 
            self.__custom_config.setLanguage('en')
            self.__custom_config.save()
            self.reload()
        lang_men.add_command(label=self.get_translation('es'), 
            command=change_lang_to_es)  
        lang_men.add_command(label=self.get_translation('en'), 
            command=change_lang_to_en)  
        self.__menubar.add_cascade(label=self.get_translation('Lang'), 
            menu=lang_men) 

        help = Menu(self.__menubar, tearoff=0)
        # Function for displaying info
        def about(): messagebox.showinfo(
            self.get_translation('Info'), 
            self.get_translation('Info1'))
        help.add_command(label=self.get_translation('Info'), command=about)  
        self.__menubar.add_cascade(label=self.get_translation('Help'), 
            menu=help)  

    def get_translation(self, key:str) -> str:
        return self.__translations.get_translation(key, 
            self.__custom_config.getLanguage())

    def clean(self):
        self.__menubar.delete(0, 5)

    def reload(self):
        self.clean()
        self.load_menu()
    
    def getMenuBar(self):
        return self.__menubar

    def setListBoxes(self, lb:ListBoxes):
        self.__l_boxes = lb