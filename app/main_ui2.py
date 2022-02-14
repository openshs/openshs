from tkinter import *
from tkinter import messagebox

window =Tk()
window.title("OpenSHS")
window.geometry("800x500")

verbose = BooleanVar()
verbose.set(False)

def enableVerbose():
    pass

darkmode = BooleanVar()
darkmode.set(False)

def darkMode():
    if darkmode.get() == 1:
        window.config(background='black')
    elif darkmode.get() == 0:
        window.config(background='white')
    else:
        messagebox.showerror('Error', 'Something went wrong!')

def about():
    messagebox.showinfo('Info', '...')

menubar = Menu(window, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')  

optionsm = Menu(menubar, tearoff=0, background='#ffcc99', foreground='black')  
optionsm.add_command(label='Generate datasets')  
optionsm.add_command(label='Tests IA')    
optionsm.add_separator()  
optionsm.add_command(label="Exit", command=window.quit)  
menubar.add_cascade(label="Options", menu=optionsm)  

toolsm = Menu(menubar, tearoff=0)  
toolsm.add_command(label="Replicate datasets") 
toolsm.add_command(label="Train IA")
menubar.add_cascade(label="Tools", menu=toolsm)  

configm = Menu(menubar, tearoff=0)
configm.add_checkbutton(label='Enable verbose', onvalue=1, offvalue=0, variable=verbose, command=enableVerbose)
menubar.add_cascade(label="Config", menu=configm)

viewm = Menu(menubar, tearoff=0)
viewm.add_checkbutton(label='Darkmode', onvalue=1, offvalue=0, variable=darkmode, command=darkMode)
menubar.add_cascade(label='View', menu=viewm)

help = Menu(menubar, tearoff=0)  
help.add_command(label="About", command=about)  
menubar.add_cascade(label="Help", menu=help)  
    
window.config(menu=menubar)
window.mainloop()