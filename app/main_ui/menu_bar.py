from tkinter import *
from tkinter import messagebox

from main_ui.context_popup import ContextPopup
from .calendar_picker import *
from .utils import *
from .aggregate_popup import *

class MenuBar:
    def __init__(self, window: Tk) :
        self.window = window
        self.l_boxes = None
        verbose = BooleanVar()
        verbose.set(False)
        # Method for enabling or disabling context information in hud view
        def enableVerbose() :
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

        self.menubar = Menu(window, foreground='black', activebackground='white', activeforeground='black')  

        optionsm = Menu(self.menubar, tearoff=0, foreground='black') 
        def genDatasets():
            if len(self.l_boxes.l_scnearios.curselection())!=0:
                # Choose date and time:
                dtPick = DateTimePicker(self.window)
                self.window.wait_window(dtPick)
                if not dtPick.cancel :
                    dt = dtPick.date+' '+dtPick.time
                    # Hide main window
                    window.withdraw()
                    startGenData(self.l_boxes.l_scnearios.get(self.l_boxes.l_scnearios.curselection()[0]), dt)
            else: 
                messagebox.showwarning('Missing context', 
                    'A context must be chosen')
            # Update list boxes
            self.l_boxes.update()
            # Show main window
            window.deiconify()
        optionsm.add_command(label='Generate datasets', command=genDatasets)  
        def testAI():
            messagebox.showwarning('Error', 
                        'Not implemented yet :(')
            """
            if len(self.l_boxes.l_ia.curselection())!=0:
                if len(self.l_boxes.l_ia.curselection())<=5:
                    # Choose context
                    ctP = ContextPopup(self.window)
                    self.window.wait_window(ctP)

                    #TODO SAVE JSON CONFIG FOR EACH AI
                    
                    if not ctP.cancel:
                        # Choose date and time:
                        dtPick = DateTimePicker(self.window)
                        self.window.wait_window(dtPick)
                        if not dtPick.cancel :
                            dt = dtPick.date+' '+dtPick.time
                            # Hide main window
                            window.withdraw()
                            startTestAI(ctP.context, dt)
                else: 
                    messagebox.showwarning('Too many mechanisms AI Mechanisms', 
                        'You can choose a maximum of 5 AI mechanisms')
            else: 
                messagebox.showwarning('Missing AI Mechanisms', 
                    'An AI mechanism must be chosen')
            """
            # Update list boxes
            self.l_boxes.update()
            # Show main window
            window.deiconify()
        optionsm.add_command(label='Tests AI', command=testAI)    
        optionsm.add_separator()  
        optionsm.add_command(label="Exit", command=window.quit)  
        self.menubar.add_cascade(label="Options", menu=optionsm)  

        toolsm = Menu(self.menubar, tearoff=0)  
        def replicateDS():
            l_aux = []
            for i in range(self.l_boxes.l_scnearios.size()):
                l_aux.append(self.l_boxes.l_scnearios.get(i))
            print(l_aux)
            if(len(l_aux)):
                agP = AgreggatePopup(self.window, l_aux)
                self.window.wait_window(agP)
                # Update list boxes
                self.l_boxes.update()
            else: 
                messagebox.showwarning('Missing contexts', 
                    'No context avilable')
        toolsm.add_command(label="Replicate datasets", command=replicateDS) 
        def trainAI():
            messagebox.showwarning('Error', 
                        'Not implemented yet :(')
        toolsm.add_command(label="Train AI", command=trainAI)
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
        
            