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
    
    print(Value[:1000])

