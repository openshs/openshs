from tkinter import *
from tkinter import messagebox

class MenuBar:
    def __init__(self, window: Tk):
        self.window = window

        verbose = BooleanVar()
        verbose.set(False)
        # Method for enabling or disabling context information in hud view
        def enableVerbose():
            #TODO
            pass

        darkmode = BooleanVar()
        darkmode.set(False)
        # Method for displaying UI components as dark or light
        def darkMode():
            if darkmode.get() == 1:
                window.config(background='black')
            elif darkmode.get() == 0:
                window.config(background='white')
            else:
                messagebox.showerror('Error', 'Something went wrong!')

        def about():
            messagebox.showinfo('Info', '...')

        self.menubar = Menu(window, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')  

        optionsm = Menu(self.menubar, tearoff=0, background='#ffcc99', foreground='black')  
        optionsm.add_command(label='Generate datasets')  
        optionsm.add_command(label='Tests IA')    
        optionsm.add_separator()  
        optionsm.add_command(label="Exit", command=window.quit)  
        self.menubar.add_cascade(label="Options", menu=optionsm)  

        toolsm = Menu(self.menubar, tearoff=0)  
        toolsm.add_command(label="Replicate datasets") 
        toolsm.add_command(label="Train IA")
        self.menubar.add_cascade(label="Tools", menu=toolsm)  

        configm = Menu(self.menubar, tearoff=0)
        configm.add_checkbutton(label='Enable verbose', onvalue=1, offvalue=0, variable=verbose, command=enableVerbose)
        self.menubar.add_cascade(label="Config", menu=configm)

        viewm = Menu(self.menubar, tearoff=0)
        viewm.add_checkbutton(label='Darkmode', onvalue=1, offvalue=0, variable=darkmode, command=darkMode)
        self.menubar.add_cascade(label='View', menu=viewm)

        help = Menu(self.menubar, tearoff=0)  
        help.add_command(label="About", command=about)  
        self.menubar.add_cascade(label="Help", menu=help)  
        
            