import pandas as pd
import re
import datetime
import numpy as np
import matplotlib.pyplot as plt
import datetime

Date_time=[]
Value=[]
Disease=[]
Stage=[]

with open('Data/AP01/Flow Events - 30-05-2024.txt') as file:
    lines=file.readlines()[5:]
    for line in lines:
        lines=line.strip()
        data=lines.split(';')
        Date_time.append(data[0])
        Value.append(data[1])
        Disease.append(data[2])
        Stage.append(data[3])

date=[]
timing=[]
for dnt in Date_time:
    number=dnt.split(' ')
    date.append(number[0])
    timing.append(number[1])

start_timing=[]
end_timing=[]

for time in timing:
    tm=time.split('-')
    start_timing.append(tm[0])
    end_timing.append(tm[1])

start_timing=pd.to_datetime(start_timing,format="%H:%M:%S,%f")
start_timing=start_timing.floor('s')

end_timing=pd.to_datetime(end_timing,format="%H:%M:%S,%f")
end_timing=end_timing.floor('s')




    





