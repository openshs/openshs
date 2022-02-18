from tkinter import *
from main_ui import *

class MainUi(Tk):
    def __init__(self):
        super().__init__()
        self.title("OpenSHS")
        self.geometry("800x500")
        self.iconbitmap("logo.ico")
        self.menu = MenuBar(self)
        self.config(menu=self.menu.menubar)

        self.grid_columnconfigure(0,weight=1) # the text and entry frames column
        self.grid_columnconfigure(2,weight=1) # the text and entry frames column
        self.grid_columnconfigure(4,weight=1) # the text and entry frames column
        self.grid_rowconfigure(1,weight=1) # all frames row
        l_boxes = ListBoxes(self)

        self.menu.l_boxes = l_boxes

def main():
    MainUi().mainloop()

if __name__ == '__main__':
    main()
