import sys
import subprocess
from tkinter import *
from tkinter import messagebox

def main():
    root = Tk()
    root.withdraw()
    try:
        with subprocess.Popen(['blender','--version'], stdout=subprocess.PIPE, universal_newlines=True) as process:
            if 'Blender 2.7' not in process.stdout.readline():
                messagebox.showerror('Error','Blender version 2.7 must be used')
                sys.exit()
    except: 
        messagebox.showerror('Error','No blender found on the system')
        sys.exit()
    
    try: root.destroy()
    except: pass
    
    if subprocess.call(['pythonw','./ui.py'], shell=False) != 0:
        messagebox.showerror('Error','Some program files are missing')
        sys.exit(-1)
    

if __name__ == '__main__':
    main()
