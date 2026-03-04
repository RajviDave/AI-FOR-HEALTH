import numpy as np
from scipy.signal import butter, filtfilt
import os
import pandas as pd

def bandpass_filter(signal, lowcut, highcut, fs, order=4):
    
    nyquist = 0.5 * fs
    
    low = lowcut / nyquist
    high = highcut / nyquist
    
    b, a = butter(order, [low, high], btype='band')
    
    filtered_signal = filtfilt(b, a, signal)
    
    return filtered_signal

def read_signals(folder):

    airflow = pd.read_csv(os.path.join(folder, "nasal_airflow.txt"))
    thoracic = pd.read_csv(os.path.join(folder, "thoracic_movement.txt"))
    spo2 = pd.read_csv(os.path.join(folder, "spo2.txt"))

    events = pd.read_csv(os.path.join(folder, "flow_events.csv"))

    return airflow, thoracic, spo2, events

