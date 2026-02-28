import pandas as pd
import re
import datetime
import numpy as np
import matplotlib.pyplot as plt
import statistics

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
mean_values = []

for i in range(0, len(Values), window):
    piece = Values[i:i+window]
    
    if len(piece)==window:
        mean = statistics.mean(piece)
        mean_values.append(mean)

min_len = min(len(mean_values), len(final_time))

rms_values = mean_values[:min_len]
final_time = final_time[:min_len]

plt.figure(figsize=(10,5))

plt.plot(final_time[:200], mean_values[:200], marker='o')

plt.xlabel("Time")
plt.ylabel("Mean Value")
plt.title("First 30 Seconds RMS")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
