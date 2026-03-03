import pandas as pd
import re
import datetime
import numpy as np
import matplotlib.pyplot as plt
import statistics

Date_time=[]
Value=[]

with open('Data/AP02/SPO2  - 30.05.2024.txt') as file:
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

Values=df['Values']
# print(Values)

window = 4
median_value=[]

for i in range(0, len(Values), window):
    piece = Values[i:i+window]
    
    if len(piece)==window:
        median=statistics.median(piece)
        median_value.append(median)
    
min_len = min(len(median_value), len(final_time))

t_spo2 = median_value[:min_len]
final_time = final_time[:min_len]

# print(len(t_spo2))
# print(len(final_time))
