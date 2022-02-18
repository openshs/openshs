from tkinter import *
import os
from tkinter import messagebox

class ContextPopup(Toplevel):
    def __init__(self, root: Tk):
        super().__init__(root)
        # Modal popup
        self.transient(root)
        self.grab_set()
        self.focus_set()
        self.title("Context Popup")
        self.geometry("360x350")
        self.resizable(width=False, height=False)
        self.cancel = True
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        #------------------------------------------------------------------------
        label = Label(self, text="Choose a context:")
        label.grid(column=0,row=0, padx=(30, 0), pady=(10, 0), sticky='NSWE')

        #------------------------------------------------------------------------
        self.scroll_sc1 = Scrollbar(self, orient=VERTICAL)
        self.scroll_sc2 = Scrollbar(self, orient=HORIZONTAL)
        self.l_scnearios = Listbox(self, yscrollcommand=self.scroll_sc1.set, 
                            xscrollcommand=self.scroll_sc2.set)
        
        self.l_scnearios.grid(column=0, row=1, padx=(30, 0), sticky='NSWE')
        self.scroll_sc1.grid(column=1, row=1, padx=(0, 15), sticky='NS')
        self.scroll_sc2.grid(column=0, row=2, padx=(30, 0), pady=(0, 30), sticky='WE')
        
        self.scroll_sc1.configure(command=self.l_scnearios.yview)
        self.scroll_sc2.configure(command=self.l_scnearios.xview)

        
        #------------------------------------------------------------------------
        def get_data():
            if len(self.l_scnearios.curselection())!=0:
                self.context = self.l_scnearios.get(self.l_scnearios.curselection()[0])
                self.cancel = False
                self.destroy()
            else:
                messagebox.showwarning('Missing context', 
                    'A context must be chosen')
        button1= Button(self, text= "Accept", command = get_data)
        button1.grid(column=0,row=3, padx=(200, 0), pady=(0, 20), sticky='NW')
        button2= Button(self, text= "Cancel", command = self.destroy)
        button2.grid(column=0,row=3, padx=(0, 20), pady=(0, 20), sticky='NE')
        
        self.update()
    
    def update(self):
        # Clear list boxes
        self.l_scnearios.delete(0,END)

        # Contexts are loaded from blender directory as files with .blend extension
        file_list = os.listdir('blender')
        for f in file_list :
            if os.path.isfile(os.path.join('blender', f)) and f.lower().endswith('.blend') \
                and not f.lower().startswith('apartment'):
                context = f.replace('.blend','')
                self.l_scnearios.insert(1, context)
