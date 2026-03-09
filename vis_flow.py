import pandas as pd
import re
import datetime
import numpy as np
import matplotlib.pyplot as plt

import os
import pandas as pd
import numpy as np


def vis_flow(folder, file):

    Date_time = []
    Value = []

    file_path = os.path.join(folder, file)

    with open(file_path) as file:
        lines = file.readlines()[7:]

        for line in lines:
            line = line.strip()
            data = line.split(';')

            Date_time.append(data[0])
            Value.append(data[1])

    df = pd.DataFrame({
        'Date_time': Date_time,
        'Values': Value
    })

    df['Date_time'] = pd.to_datetime(
        df['Date_time'],
        format="%d.%m.%Y %H:%M:%S,%f"
    )

    df['Date_time'] = df['Date_time'].dt.floor('s')

    final_time = df['Date_time'].drop_duplicates().tolist()

    df['Values'] = pd.to_numeric(df['Values'], errors='coerce')

    flow_values = df['Values']

    window = 32
    rms_values = []

    for i in range(0, len(flow_values), window):

        piece = flow_values[i:i+window]

        if len(piece) == window:
            rms = np.sqrt(np.mean(piece**2))
            rms_values.append(rms)

    min_len = min(len(rms_values), len(final_time))

    rms_values = rms_values[:min_len]
    t_flow = final_time[:min_len]

    return t_flow, rms_values