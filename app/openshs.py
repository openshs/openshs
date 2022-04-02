from tkinter import *
from main_ui.menu_bar import *
from main_ui.list_boxes import *
from config.config import *
from config.translations import Translations
import subprocess
import sys

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
        l_boxes = ListBoxes(self, custom_config)

        # MenuBar can make changes to ListBoxes
        self.__menu.setListBoxes(l_boxes)

def main():
    root = Tk()
    root.withdraw()
    try:
        with subprocess.Popen(['blender','--version'], stdout=subprocess.PIPE, universal_newlines=True) as process:
            if 'Blender 2.7' not in process.stdout.readline():
                messagebox.showerror('Error','Blender version 2.7 must be used')
                sys.exit()
    except: 
        messagebox.showerror('Error','No blender found on the system')
        exit()

    try:
        with subprocess.Popen(['python','--version'], stdout=subprocess.PIPE, universal_newlines=True) as process:
            if 'Python 3' not in process.stdout.readline():
                messagebox.showerror('Error','Python 3 must be used')
                sys.exit()
    except: 
        messagebox.showerror('Error','No python found on the system')
        exit()
    
    try: root.destroy()
    except: pass

    MainUi().mainloop()
    # DEPRECATED
    #if subprocess.call(['pythonw','./main_ui.py'], shell=False) != 0:
    #    messagebox.showerror('Error','Some program files are missing')
    #    sys.exit(-1)
    

if __name__ == '__main__':
    main()
