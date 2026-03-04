import numpy as np
from scipy.signal import butter, filtfilt
import pandas as pd

from vis_flow import rms_values
from vis_spo2 import median_values
from vis_thorac import mean_values
from vis_eventflow import Disease, start_timing, end_timing


# -------------------------------
# Bandpass Filter
# -------------------------------
def bandpass_filter(signal, lowcut, highcut, fs, order=4):

    signal = np.array(signal)

    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist

    b, a = butter(order, [low, high], btype='band')

    filtered_signal = filtfilt(b, a, signal)

    return filtered_signal

bandpass=bandpass_filter(rms_values,0.17,0.4,32,4)

# -------------------------------
# Preprocess signals
# -------------------------------
def preprocess_signals(airflow):

    airflow = bandpass_filter(
        airflow,
        0.17,
        0.4,
        fs=32
    )

    return airflow

preprocess=preprocess_signals(rms_values)
# print(preprocess[:25])
# print(len(preprocess))


# # -------------------------------
# # Window creation
# # -------------------------------
def create_windows(signal, fs, window_sec=30, overlap=0.5):

    window_size = int(window_sec * fs)
    step = int(window_size * (1 - overlap))

    windows = []

    for start in range(0, len(signal) - window_size, step):

        end = start + window_size

        windows.append(signal[start:end])

    return windows

window=create_windows(rms_values,32,30,0.5)

# # -------------------------------
# # Label windows
# # -------------------------------

def label_window(start, end):

    for i in range(len(Disease)):

        event_start = start_timing[i].timestamp()
        event_end = end_timing[i].timestamp()

        overlap = max(0, min(end, event_end) - max(start, event_start))

        window_len = end - start

        if overlap / window_len > 0.5:
            return Disease[i]

    return event_start

# # -------------------------------
# # MAIN PIPELINE
# # -------------------------------

# # convert to numpy
airflow = np.array(rms_values)
thoracic = np.array(mean_values)
spo2 = np.array(median_values)


# filter breathing signals
airflow, thoracic = preprocess_signals(airflow, thoracic)


# create windows
airflow_windows = create_windows(airflow, fs=32)
thoracic_windows = create_windows(thoracic, fs=32)
spo2_windows = create_windows(spo2, fs=4)


labels = []

for i in range(len(airflow_windows)):

    start_time = i * 15
    end_time = start_time + 30

    label = label_window(start_time, end_time)

    labels.append(label)


# build dataset
dataset = []

for i in range(len(airflow_windows)):

    row = {
        "airflow": airflow_windows[i],
        "thoracic": thoracic_windows[i],
        "spo2": spo2_windows[i],
        "label": labels[i]
    }

    dataset.append(row)


df = pd.DataFrame(dataset)


# save dataset
df.to_pickle("Dataset/breathing_dataset.pkl")