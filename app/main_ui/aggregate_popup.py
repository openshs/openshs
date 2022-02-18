from tkinter import *
from tkinter.ttk import Progressbar
from click import progressbar
from tkcalendar import *
from datetime import datetime
from .utils import *

class AgreggatePopup(Toplevel):
   def __init__(self, root, contexts) :
      super().__init__(root)
      # Modal popup
      self.transient(root)
      self.grab_set()
      self.focus_set()
      self.title("Aggregate Datasets")
      self.geometry("340x370")
      self.resizable(width=False, height=False)
      
      self.cancel = True
      self.days = None
      self.date = None
      self.margin = None
      self.is_var = False

      label1 = Label(self, text="Choose date:")
      label1.place(x=130, y=10)

      # Date  Picker:
      cal= Calendar(self, selectmode="day", date_pattern='yyyy-mm-dd',
         year=datetime.now().year, 
         month=datetime.now().month, 
         day=datetime.now().day
      )
      cal.place(x=40, y=40)

      label2 = Label(self, text="Number of days:")
      label2.place(x=70, y=240)

      label3 = Label(self, text="Margin minutes:")
      label3.place(x=70, y=270)
      
      self.daysstr = StringVar(self, 1)
      self.daysSB = Spinbox(self,from_=0,to=1000,wrap=True,textvariable=self.daysstr,width=4)

      self.marginstr = StringVar(self, 0)
      self.marhinSB = Spinbox(self,from_=0,to=1000,wrap=True,textvariable=self.marginstr,width=4)    # ,state="readonly"
      
      self.daysSB.place(x=180, y=240)
      self.marhinSB.place(x=180, y=270)
      
      var1 = IntVar()
      def changeVar():
         if (var1.get() == 0): self.is_var = False
         else: self.is_var = True
      Checkbutton(self, text='Variable Activities',variable=var1, onvalue=1, offvalue=0, command=changeVar)\
         .place(x=120, y=300)

      self.progress_bar = Progressbar(self, orient=HORIZONTAL, length=160, mode='determinate')
      self.progress_bar.place(x=20, y=340)

      # Function to select the date
      def get_data():
         self.date = cal.get_date()
         self.days = int(self.daysstr.get())
         self.margin = int(self.marginstr.get())
         aggregate(
            contexts, 
            self.days,
            self.date,
            self.margin,
            self.is_var,
            self.progress_bar,
            self
         )
         self.destroy()
      
      button1= Button(self, text= "Accept", command = get_data)
      button1.place(x=190, y=340)
      
      button2= Button(self, text= "Cancel", command = self.destroy)
      button2.place(x=250, y=340)