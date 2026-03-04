from scipy.signal import butter, filtfilt
from plotting import airflow_trim,thoracic_trim

def bandpass_filter(signal, fs, lowcut=0.17, highcut=0.4, order=4):
    nyquist = fs / 2
    low = lowcut / nyquist
    high = highcut / nyquist

    b, a = butter(order, [low, high], btype='band')
    filtered_signal = filtfilt(b, a, signal)

    return filtered_signal

fs = 32
airflow_filtered = bandpass_filter(airflow_trim, fs)
thoracic_filtered = bandpass_filter(thoracic_trim, fs)

print(airflow_filtered[:25])
print(thoracic_filtered[:25])