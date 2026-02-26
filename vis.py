import pandas as pd
import matplotlib.pyplot as plt
import re
import datetime

date=[]
time=[]
values=[]

with open('Data/AP01/Flow - 30-05-2024.txt','r') as f:
    lines=f.readlines()[7:]
    for line in lines:
        line=line.strip()
        data=line.split(' ')
        date.append(data[0])
        time.append(data[1])
        values.append(data[2])
df=pd.DataFrame({'Date':date,'Time':time,'Values':values})
df['Time']=pd.to_datetime(df['Time'],format='%H:%M:%S,%f;')
df['Time']=df['Time'].dt.floor('min')
print(df['Time'])