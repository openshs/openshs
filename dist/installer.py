import subprocess
import sys
import os
import shutil

if os.path.exists("app"): shutil.rmtree("app")
if os.path.exists("build"): shutil.rmtree("build")
if os.path.exists("dist"): shutil.rmtree("dist")

shutil.copytree(os.path.join("..","app"), os.path.join(".","app"))

if subprocess.call('pyinstaller --clean --noconfirm --onefile --windowed --icon "app/logo.ico"  "app/openshs.py"', shell=False) != 0:
    print("Error con pyinstaller")
    sys.exit()

if os.path.exists("build"): shutil.rmtree("build")

for root, dirs, files in os.walk("app"):
    for file in files:
        file = os.path.join(root, file)
        if ".py" in file and not "blender" in file: os.remove(file)
    for dir in dirs:
        if dir.endswith('__pycache__'):
            dir = os.path.join(root, dir)
            shutil.rmtree(dir)

if os.path.exists(os.path.join("app","main_ui")): 
    shutil.rmtree(os.path.join("app","main_ui"))
if os.path.exists(os.path.join("app","repeater")): 
    shutil.rmtree(os.path.join("app","repeater"))

for root, dirs, files in os.walk("dist"):
    for file in files:
        file = os.path.join(root, file)
        shutil.copy(file, "app")

if os.path.exists("dist"): shutil.rmtree("dist")
if os.path.exists("openshs.spec"): os.remove("openshs.spec")

#pyinstaller --clean --noconfirm --onefile --windowed --icon "../app/logo.ico"  "../app/ui.py"