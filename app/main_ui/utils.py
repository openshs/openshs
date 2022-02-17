from datetime import datetime
import json
import os
import subprocess
from tkinter import messagebox

CONFIG_PATH = os.path.join('config','config.json')
CONFIG = {}

def is_weekday(dt):
    if dt.weekday() < 5:
        return True
    else:
        return False

def start(context, date_time):
    start_dt = datetime.strptime(date_time, 
            "%Y-%m-%d %H-%M-%S")

    weekday_p = is_weekday(start_dt)

    # Write the starting datetime for blender to read
    start_time = int(start_dt.timestamp())
    # Serializing json 
    json_object = json.dumps(CONFIG, indent = 4)
    # Writing to sample.json
    with open(CONFIG_PATH, "w") as json_file:
        json_file.write(json_object)

    subprocess.call(["blender", os.path.join('blender',context+'.blend')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # After the simulation is complete, data stored in the output.csv file must be saved
    count = 0
    while True:
        try:
            data_week_csv = os.path.join('data', 
                ('weekday_' if weekday_p else 'weekend_') + context + '_' + datetime.strftime(start_dt, "%Y-%m-%d %H-%M-%S") +
                ('' if not count else '_' + str(count) ) + '.csv')
            data_out_csv = os.path.join('temp', 'output.csv')
            os.rename(data_out_csv, data_week_csv)
            messagebox.showinfo('Info', 'Dataset saved as  ' + data_week_csv); break
        except FileExistsError:
            messagebox.showinfo('Info', 'File ' + data_week_csv +  ' already exists')
            count+=1
        except FileNotFoundError:
            messagebox.showinfo('Info', 'Ungenerated dataset'); break