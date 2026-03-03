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

Values=df['Values']
# print(Values)

window = 32
rms_values = []

for i in range(0, len(Values), window):
    piece = Values[i:i+window]
    
    if len(piece)==window:
        rms = np.sqrt(np.mean(piece**2))
        rms_values.append(rms)

min_len = min(len(rms_values), len(final_time))

t_flow = rms_values[:min_len]
final_time = final_time[:min_len]

print(len(t_flow))
print(len(final_time))