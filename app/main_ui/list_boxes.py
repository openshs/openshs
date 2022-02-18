from tkinter import *
import os

class ListBoxes:
    def __init__(self, window: Tk):
        self.window = window
        
        #------------------------------------------------------------------------
        label = Label(self.window, text="Contexts:")
        label.config(font=("Times New Roman",14))
        label.grid(column=0,row=0, padx=(30, 0), pady=(10, 0), sticky='NSWE')

        #------------------------------------------------------------------------
        label = Label(self.window, text="Datasets:")
        label.config(font=("Times New Roman",14))
        label.grid(column=2,row=0, padx=(15, 0), pady=(10, 0), sticky='NSWE')

        #------------------------------------------------------------------------
        label = Label(self.window, text="AI Mechanisms:")
        label.config(font=("Times New Roman",14))
        label.grid(column=4,row=0, padx=(15, 0), pady=(10, 0), sticky='NSWE')

        #------------------------------------------------------------------------
        self.scroll_sc1 = Scrollbar(self.window, orient=VERTICAL)
        self.scroll_sc2 = Scrollbar(self.window, orient=HORIZONTAL)
        self.l_scnearios = Listbox(self.window, yscrollcommand=self.scroll_sc1.set, 
                            xscrollcommand=self.scroll_sc2.set)
        
        self.l_scnearios.grid(column=0, row=1, padx=(30, 0), sticky='NSWE')
        self.scroll_sc1.grid(column=1, row=1, padx=(0, 15), sticky='NS')
        self.scroll_sc2.grid(column=0, row=2, padx=(30, 0), pady=(0, 30), sticky='WE')
        
        self.scroll_sc1.configure(command=self.l_scnearios.yview)
        self.scroll_sc2.configure(command=self.l_scnearios.xview)

        #------------------------------------------------------------------------
        self.scroll_ds1 = Scrollbar(self.window, orient=VERTICAL)
        self.scroll_ds2 = Scrollbar(self.window, orient=HORIZONTAL)
        self.l_datast = Listbox(self.window, yscrollcommand=self.scroll_ds1.set, 
                            xscrollcommand=self.scroll_ds2.set)
        
        self.l_datast.grid(column=2,row=1, padx=(15, 0), sticky='NSWE')
        self.scroll_ds1.grid(column=3, row=1, padx=(0, 15), sticky='NS')
        self.scroll_ds2.grid(column=2, row=2, padx=(15, 0), pady=(0, 30), sticky='WE')
        
        self.scroll_ds1.configure(command=self.l_datast.yview)
        self.scroll_ds2.configure(command=self.l_datast.xview)
        
        

        #------------------------------------------------------------------------
        self.scroll_ia1 = Scrollbar(self.window, orient=VERTICAL)
        self.scroll_ia2 = Scrollbar(self.window, orient=HORIZONTAL)
        self.l_ia = Listbox(self.window, selectmode=MULTIPLE, yscrollcommand=self.scroll_ia1.set, 
                            xscrollcommand=self.scroll_ia2.set)
        
        self.l_ia.grid(column=4,row=1, padx=(15, 0), sticky='NSWE')
        self.scroll_ia1.grid(column=5, row=1, padx=(0, 30), sticky='NS')
        self.scroll_ia2.grid(column=4, row=2, padx=(15, 0), pady=(0, 30), sticky='WE')      
        
        self.scroll_ia1.configure(command=self.l_ia.yview)
        self.scroll_ia2.configure(command=self.l_ia.xview)       
        
        self.update()
    
    def update(self):
        # Clear list boxes
        self.l_scnearios.delete(0,END)
        self.l_datast.delete(0,END)
        self.l_ia.delete(0,END)

        # Contexts are loaded from blender directory as files with .blend extension
        file_list = os.listdir('blender')
        for f in file_list :
            if os.path.isfile(os.path.join('blender', f)) and f.lower().endswith('.blend') \
                and not f.lower().startswith('apartment'):
                context = f.replace('.blend','')
                self.l_scnearios.insert(1, context)

        # Contexts are loaded from blender directory as files with .blend extension
        file_list = os.listdir('data')
        for f in file_list :
            if os.path.isfile(os.path.join('data', f)) and f.lower().endswith('.csv') :
                data = f.replace('.csv','')
                self.l_datast.insert(1, data)
        
        # Contexts are loaded from blender directory as files with .blend extension
        file_list = os.listdir('ia_mech')
        for f in file_list :
            if os.path.isfile(os.path.join('ia_mech', f)) and f.lower().endswith('.json') :
                data = f.replace('.json','')
                self.l_ia.insert(1, data)