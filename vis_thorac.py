import pandas as pd
import re
import datetime
import numpy as np
import matplotlib.pyplot as plt
import statistics
import os

def thorac(folder,file):

    Date_time=[]
    Value=[]

    file_path = os.path.join(folder, file)

    with open(file_path) as file:

        lines=file.readlines()[7:]
        for line in lines:
            lines=line.strip()
            data=lines.split(';')
            Date_time.append(data[0])
            Value.append(data[1])
            
    df=pd.DataFrame({'Date_time':Date_time,'Values':Value})
    df['Date_time']=pd.to_datetime(df['Date_time'],format="%d.%m.%Y %H:%M:%S,%f")

    df['Date_time']=df['Date_time'].dt.floor('s')

    final_time=[]
    final_time=df['Date_time'].drop_duplicates().tolist()

    df['Values']=pd.to_numeric(df['Values'],errors='coerce')

    thoracic_values=df['Values']

    window = 32
    mean_values = []

    for i in range(0, len(thoracic_values), window):
        piece = thoracic_values[i:i+window]
        
        if len(piece)==window:
            mean = statistics.mean(piece)
            mean_values.append(mean)

    min_len = min(len(mean_values), len(final_time))

    mean_values = mean_values[:min_len]
    t_thorac = final_time[:min_len]

    return t_thorac,mean_values

import os

def thorac_values(folder_path):

    thorac_time = []
    thorac_values = []

    file_path = os.path.join(folder_path, "thorac.txt")

    with open(file_path, "r") as file:

        lines = file.readlines()[7:]   # skip header lines

        for line in lines:
            line = line.strip()
            data = line.split(';')

            thorac_time.append(data[0])
            thorac_values.append(data[1])

    return thorac_time, thorac_values

