from datetime import datetime, timedelta
import csv
import json
import os
import subprocess
from tkinter import messagebox
from glob import glob
from random import randrange, choice
import time
from config.config import Config
from recognition.rec_thread import Assistant
from repeater import *

def is_weekday(dt):
    if dt.weekday() < 5:
        return True
    else:
        return False

def add_timestamp_field(reader, start_dt):
    if type(start_dt) is str:
        start_dt = datetime.strptime(start_dt, "%Y-%m-%d %H-%M-%S")
    ts = start_dt
    asec = timedelta(seconds=1)
    result = []

    for i in reader:
        row = i + [ts.strftime("%Y-%m-%d %H-%M-%S")]
        result.append(row)
        ts += asec
    return result

def random_timestamp(dt, pool_files, time_margin):
    pool_times = [x.split(' ')[1].split('_')[0].replace('.csv','') for x in pool_files]
    times = [datetime.strptime(x, "%H-%M-%S") for x in pool_times]
    random_sample = choice(times)
    if time_margin > 0:
        margin = timedelta(seconds=time_margin * 60)
        random_sample = random_date(random_sample - (margin/2), random_sample + (margin/2))
    new_dt = datetime(dt.year, dt.month, dt.day, random_sample.hour, random_sample.minute, random_sample.second)
    return new_dt

def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

"""
    Function to start simulation and generate datasets
"""
def startGenData(context, date_time, custom_config: Config):
    start_dt = datetime.strptime(date_time, 
            "%Y-%m-%d %H-%M-%S")

    weekday_p = is_weekday(start_dt)

    # Write the starting datetime for blender to read
    custom_config.setStartTime(int(start_dt.timestamp()))
    custom_config.save()
    
    bl_file = os.path.join('blender',context+'.blend')
    if not os.path.isfile(bl_file): return False
    
    assistant = Assistant(int(start_dt.timestamp()), custom_config.getLanguage()); assistant.start()
    subprocess.call(["blender", bl_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, 
        shell=False)
    assistant.end()
    
    # After the simulation is complete, data stored in the output.csv file must be saved
    count = 0
    while True:
        try:
            data_week_csv = os.path.join('data', 
                ('weekday_' if weekday_p else 'weekend_') + context + '_' + datetime.strftime(start_dt, "%Y-%m-%d %H-%M-%S") +
                ('' if not count else '_' + str(count) ) + '.csv')
            data_out_csv = os.path.join('temp', 'output.csv')
            os.rename(data_out_csv, data_week_csv)
            messagebox.showinfo('Info', 'Dataset saved in: ' + data_week_csv); break
        except FileExistsError:
            messagebox.showinfo('Info', 'File ' + data_week_csv +  ' already exists')
            count+=1
        except FileNotFoundError:
            messagebox.showinfo('Info', 'Ungenerated dataset'); break
    return True

"""
    Function to start simulation in interactive mode
"""
def startIntMode(context, custom_config: Config):
    # Write the starting datetime for blender to read
    custom_config.setStartTime(int(datetime.now().timestamp()))
    custom_config.save()
    
    bl_file = os.path.join('blender',context+'.blend')
    if not os.path.isfile(bl_file): return False 

    assistant = Assistant(custom_config.getStartTime(), custom_config.getLanguage()); assistant.start()
    subprocess.call(["blender", bl_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, 
        shell=False)
    assistant.end()
    return True

"""
    Function to group simulation data into a dataset file
"""
def aggregate(contexts, days, start_date, time_margin, variable_activities, progress_bar, ws):
    files = glob(os.path.join('data','*.csv'))

    aday = timedelta(days=1)
    dt = datetime.strptime(start_date, "%Y-%m-%d")

    # The header row
    with open(files[0], 'r') as headfile:
        csv_reader = csv.reader(headfile)
        header = next(csv_reader)
    header.append('timestamp')

    d_rows = []
    with open(os.path.join('datasets','dataset.csv'), 'w') as outf:
        csv_writer = csv.writer(outf)
        csv_writer.writerow(header)

        for d in range(days):
            if is_weekday(dt):
                for context in contexts:
                    pool_files = glob('data/weekday_' + context + '*.csv')
                    if len(pool_files):
                        pool = SamplesPool(pool_files, variable_activities)
                        rep_rows = pool.generate_sample(header=False)
                        d_rows += add_timestamp_field(rep_rows, random_timestamp(dt, pool_files, time_margin))
            else:
                for context in contexts:
                    pool_files = glob('data/weekend_' + context + '*.csv')
                    if len(pool_files):
                        pool = SamplesPool(pool_files, variable_activities)
                        rep_rows = pool.generate_sample(header=False)
                        d_rows += add_timestamp_field(rep_rows, random_timestamp(dt, pool_files, time_margin))
            dt += aday
            
            progress_bar['value']=int((d+1)/days)*100
            ws.update()
            time.sleep(0.1)

        csv_writer.writerows(d_rows)
