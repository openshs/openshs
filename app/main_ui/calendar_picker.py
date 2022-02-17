from tkinter import *
from tkcalendar import *
from datetime import datetime

class DateTimePicker(Toplevel):
   def __init__(self, root) :
      super().__init__(root)
      self.title("DateTime Picker")
      self.geometry("360x350")
      self.resizable(width=False, height=False)
      
      self.cancel = True
      self.date = None
      self.time = None

      label1 = Label(self, text="Choose date:")
      label1.place(x=150, y=10)

      # Date  Picker:
      cal= Calendar(self, selectmode="day", date_pattern='yyyy-mm-dd',
         year=datetime.now().year, 
         month=datetime.now().month, 
         day=datetime.now().day
      )
      cal.place(x=60, y=40)

      # Function to select the date
      def get_date():
         self.date = cal.get_date()
         print(cal.get_date())
         self.time = "-".join(
            [self.hourstr.get(),
            self.minstr.get(),
            self.secstr.get()]
         )
         self.cancel = False
         self.destroy()

      label2 = Label(self, text="Choose time (hours | minutes | seconds):")
      label2.place(x=70, y=240)

      self.hourstr = StringVar(self,datetime.now().hour)
      self.hour = Spinbox(self,from_=0,to=23,wrap=True,textvariable=self.hourstr,width=2,state="readonly")

      self.minstr = StringVar(self,datetime.now().minute)
      self.min = Spinbox(self,from_=0,to=59,wrap=True,textvariable=self.minstr,width=2)    # ,state="readonly"
      
      self.secstr = StringVar(self, datetime.now().second)
      self.sec = Spinbox(self,from_=0,to=59,wrap=True,textvariable=self.secstr,width=2) 

      self.last_valueSec = ""
      self.last_value = ""

      self.minstr.trace("w",self.trace_var)
      self.secstr.trace("w",self.trace_varsec)

      self.hour.place(x=140, y=270)
      self.min.place(x=170, y=270)
      self.sec.place(x=200, y=270)
      
      button1= Button(self, text= "Accept", command = get_date)
      button1.place(x=160, y=310)

   def trace_var(self,*args):
      if self.last_value == "59" and self.minstr.get() == "0":
         self.hourstr.set(int(self.hourstr.get())+1 if self.hourstr.get() !="23" else 0)   
      self.last_value = self.minstr.get()

   def trace_varsec(self,*args):
      if self.last_valueSec == "59" and self.secstr.get() == "0":
         self.minstr.set(int(self.minstr.get())+1 if self.minstr.get() !="59" else 0)
         if self.last_value == "59":
            self.hourstr.set(int(self.hourstr.get())+1 if self.hourstr.get() !="23" else 0)            
      self.last_valueSec = self.secstr.get()
