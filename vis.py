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

df['Values']=pd.to_numeric(df['Values'])
for i in range(0,len(df['Values']),window):
    piece=df['Values'][i:i+window]
    
    if len(piece)== window:
        rms = np.sqrt(np.mean(np.square(piece)))
        rms_values.append(rms)

print(len(rms_values))
    