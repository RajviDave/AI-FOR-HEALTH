import pandas as pd
import matplotlib.pyplot as plt
import re
import datetime
import statistics 
import numpy as np

date_time=[]
values=[]
window =32
rms_values=[]

with open('Data/AP01/Flow - 30-05-2024.txt','r') as f:
    lines=f.readlines()[7:]
    for line in lines:
        line=line.strip()
        data=line.split(';')
        date_time.append(data[0])
        values.append(data[1])
df=pd.DataFrame({'Date_Time':date_time,'Values':values})
df['Date_Time']=pd.to_datetime(df['Date_Time'], format="%d.%m.%Y %H:%M:%S,%f")
df['Date_Time']=df['Date_Time'].dt.floor("s")
df['Values'] = pd.to_numeric(df['Values'], errors='coerce')

df = df.dropna(subset=['Values'])

values = df['Values'].to_numpy()

window = 32
rms_values = []

for i in range(0, len(values), window):
    piece = values[i:i+window]
    
    if len(piece)==window:
        rms = np.sqrt(np.mean(piece**2))
        rms_values.append(rms)

final_time = df['Date_Time'].drop_duplicates().tolist()

print(len(final_time))
print(rms_values[:10])
    