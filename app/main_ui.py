from tkinter import *
from main_ui import *

window =Tk()
window.title("OpenSHS")
window.geometry("800x500")

menu = MenuBar(window)
window.config(menu=menu.menubar)

window.grid_columnconfigure(0,weight=1) # the text and entry frames column
window.grid_columnconfigure(2,weight=1) # the text and entry frames column
window.grid_columnconfigure(4,weight=1) # the text and entry frames column
window.grid_rowconfigure(1,weight=1) # all frames row
l_boxes = ListBoxes(window)

menu.l_boxes = l_boxes

window.mainloop()