from tkinter import *
from main_ui import *

window =Tk()
window.title("OpenSHS")
window.geometry("800x500")

menu = MenuBar(window)

window.config(menu=menu.menubar)

window.mainloop()