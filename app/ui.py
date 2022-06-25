from tkinter import *
from main_ui.menu_bar import *
from main_ui.list_boxes import *
from config.config import *
from config.translations import Translations

class MainUi(Tk):
    def __init__(self):
        super().__init__()
        self.title("OpenSHS")
        self.geometry("800x500")
        self.iconbitmap("logo.ico")
        
        # Load custom settings for simulation
        custom_config = Config()
        # Load transaltions
        translations = Translations()

        self.__menu = MenuBar(self, custom_config, translations)
        self.config(menu=self.__menu.getMenuBar())

        # Grid spaces are adjusted for components
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)
        l_boxes = ListBoxes(self, custom_config, translations)

        # MenuBar can make changes to ListBoxes
        self.__menu.setListBoxes(l_boxes)

def main():
    MainUi().mainloop()

if __name__ == '__main__':
    main()
