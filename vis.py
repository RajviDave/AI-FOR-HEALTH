import pandas as pd
import re
import datetime

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
print(len(final_time))

