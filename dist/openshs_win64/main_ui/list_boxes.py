from tkinter import *
import os
from config.config import Config
from config.translations import Translations

class ListBoxes:
    def __init__(self, window: Tk, custom_config: Config, translations : Translations):
        self.__window = window
        self.__custom_config = custom_config
        self.__translations = translations
        
        #------------------------------------------------------------------------
        self.__label1 = Label(self.__window, 
            text=self.get_translation("Contexts")+":")
        self.__label1.config(font=("Times New Roman",14))
        self.__label1.grid(column=0,row=0, padx=(30, 0), pady=(10, 0), sticky='NSWE')

        #------------------------------------------------------------------------
        self.__label2 = Label(self.__window, 
            text=self.get_translation("Datasets")+":")
        self.__label2.config(font=("Times New Roman",14))
        self.__label2.grid(column=2,row=0, padx=(15, 0), pady=(10, 0), sticky='NSWE')
        
        #------------------------------------------------------------------------
        scroll_sc1 = Scrollbar(self.__window, orient=VERTICAL)
        scroll_sc2 = Scrollbar(self.__window, orient=HORIZONTAL)
        self.__l_scnearios = Listbox(self.__window, yscrollcommand=scroll_sc1.set, 
                            xscrollcommand=scroll_sc2.set)
        
        self.__l_scnearios.grid(column=0, row=1, padx=(30, 0), sticky='NSWE')
        scroll_sc1.grid(column=1, row=1, padx=(0, 15), sticky='NS')
        scroll_sc2.grid(column=0, row=2, padx=(30, 0), pady=(0, 30), sticky='WE')
        
        scroll_sc1.configure(command=self.__l_scnearios.yview)
        scroll_sc2.configure(command=self.__l_scnearios.xview)

        #------------------------------------------------------------------------
        scroll_ds1 = Scrollbar(self.__window, orient=VERTICAL)
        scroll_ds2 = Scrollbar(self.__window, orient=HORIZONTAL)
        self.__l_datast = Listbox(self.__window, yscrollcommand=scroll_ds1.set, 
                            xscrollcommand=scroll_ds2.set)
        
        self.__l_datast.grid(column=2,row=1, padx=(15, 0), sticky='NSWE')
        scroll_ds1.grid(column=3, row=1, padx=(0, 30), sticky='NS')
        scroll_ds2.grid(column=2, row=2, padx=(15, 0), pady=(0, 30), sticky='WE')
        
        scroll_ds1.configure(command=self.__l_datast.yview)
        scroll_ds2.configure(command=self.__l_datast.xview)     
        
        self.update()
    
    def getLEscenarios(self):
        return self.__l_scnearios
    
    def update(self):
        # Clear list boxes
        self.__l_scnearios.delete(0,END)
        self.__l_datast.delete(0,END)

        # Contexts are loaded from the Config object
        for context in self.__custom_config.getContexts() :
            self.__l_scnearios.insert(1, context)

        # Datasets are loaded from data directory as files with .csv extension
        file_list = os.listdir('data')
        for f in file_list :
            if os.path.isfile(os.path.join('data', f)) and f.lower().endswith('.csv') :
                data = f.replace('.csv','')
                self.__l_datast.insert(1, data)
    
    def reload(self):
        self.__label1.config(text=self.get_translation("Contexts")+":")
        self.__label2.config(text=self.get_translation("Datasets")+":")
    
    """
        A shortcut for the translations.get_translations
    """
    def get_translation(self, key:str) -> str:
        return self.__translations.get_translation(key, 
            self.__custom_config.getLanguage())
