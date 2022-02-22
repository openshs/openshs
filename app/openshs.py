import subprocess
from tkinter import Tk
from tkinter import messagebox
import sys

def main() :
    root = Tk()
    root.withdraw()
    try:
        with subprocess.Popen(['blender','--version'], stdout=subprocess.PIPE, universal_newlines=True) as process:
            if 'Blender 2.7' not in process.stdout.readline():
                messagebox.showerror('Error','Blender version 2.7 must be used')
                sys.exit(-1)
    except: 
        messagebox.showerror('Error','No blender found on the system')
        exit(-1)

    try:
        with subprocess.Popen(['python','--version'], stdout=subprocess.PIPE, universal_newlines=True) as process:
            if 'Python 3' not in process.stdout.readline():
                messagebox.showerror('Error','Python 3 must be used')
                sys.exit(-1)
    except: 
        messagebox.showerror('Error','No python found on the system')
        exit(-1)

    
    if subprocess.call(['pythonw','./main_ui.py'], shell=False) != 0:
        messagebox.showerror('Error','Some program files are missing')
        sys.exit(-1)
    
    try: root.destroy()
    except: pass

if __name__ == '__main__' :
    main()
