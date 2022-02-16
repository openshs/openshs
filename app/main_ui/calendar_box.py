#Import the libraries
from tkinter import *
from tkcalendar import *

#Create an instance of tkinter frame or window
win= Tk()
win.title("Calendar")
win.geometry("700x600")

cal= Calendar(win, selectmode="day",year= 2021, month=3, day=3)
cal.pack(pady=20)

#Define Function to select the date
def get_date():
   label.config(text=cal.get_date())

#Create a button to pick the date from the calendar
button= Button(win, text= "Select the Date", command= get_date)
button.pack(pady=20)

#Create Label for displaying selected Date
label= Label(win, text="")
label.pack(pady=20)

win.mainloop()