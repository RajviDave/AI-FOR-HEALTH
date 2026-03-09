import pandas as pd
import re
import datetime
import numpy as np
import matplotlib.pyplot as plt

Date_time=[]
Value=[]

with open('Data/AP01/Flow - 30-05-2024.txt') as file:
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

flow_values=df['Values']

window = 32
rms_values = []

for i in range(0, len(flow_values), window):
    piece = flow_values[i:i+window]
    
    if len(piece)==window:
        rms = np.sqrt(np.mean(piece**2))
        rms_values.append(rms)

min_len = min(len(rms_values), len(final_time))

rms_values = rms_values[:min_len]
t_flow = final_time[:min_len]


