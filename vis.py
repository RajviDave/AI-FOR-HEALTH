import pandas as pd
import re

with open('Data/AP01/Flow - 30-05-2024.txt','r') as file:
    lines = file.readlines()[7:]
    for line in lines:
        line=line.strip()
        data=line.split(';')