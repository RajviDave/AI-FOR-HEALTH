import numpy as np
from scipy.signal import butter, filtfilt

def bandpass_filter(signal, fs=32, lowcut=0.17, highcut=0.4, order=4):
    nyquist = 0.5 * fs
    
    low = lowcut / nyquist
    high = highcut / nyquist
    
    b, a = butter(order, [low, high], btype='band')
    
    filtered_signal = filtfilt(b, a, signal)
    
    return filtered_signal