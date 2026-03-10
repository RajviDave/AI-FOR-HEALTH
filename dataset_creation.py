import os
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt
import argparse

from vis_flow import values
from vis_thorac import thorac_values

dataset_rows = []

parser = argparse.ArgumentParser()

parser.add_argument("-in_dir", required=True, help="Input Data Directory")
parser.add_argument("-out_dir", required=True, help="Output Dataset Directory")

args = parser.parse_args()

data_dir = args.in_dir
out_dir = args.out_dir

participants = sorted(os.listdir(data_dir))
# -----------------------------
# Bandpass Filter
# -----------------------------
def bandpass_filter(signal, lowcut, highcut, fs, order=4):

    nyquist = fs / 2
    low = lowcut / nyquist
    high = highcut / nyquist

    b, a = butter(order, [low, high], btype='band')

    filtered_signal = filtfilt(b, a, signal)

    return filtered_signal


# -----------------------------
# Window Creation
# -----------------------------
def create_windows(flow_signal, thoracic_signal, fs=32, window_sec=30, overlap=0.5):

    window_size = int(fs * window_sec)
    step_size = int(window_size * (1 - overlap))

    windows = []

    signal_length = len(flow_signal)

    for start in range(0, signal_length - window_size, step_size):

        end = start + window_size

        flow_window = flow_signal[start:end]
        thoracic_window = thoracic_signal[start:end]

        window = np.stack((flow_window, thoracic_window), axis=1)

        windows.append((window, start, end))

    return windows


# -----------------------------
# Label Function
# -----------------------------
def label_window(window_start, window_end, events_df):

    window_duration = (window_end - window_start).total_seconds()

    best_label = "Normal"
    max_overlap = 0

    for _, event in events_df.iterrows():

        event_start = event["start_time"]
        event_end = event["end_time"]
        event_label = event["event"]

        overlap_start = max(window_start, event_start)
        overlap_end = min(window_end, event_end)

        overlap = (overlap_end - overlap_start).total_seconds()

        if overlap > 0:
            if overlap > max_overlap:
                max_overlap = overlap
                best_label = event_label

    if max_overlap >= 0.5 * window_duration:
        return best_label
    else:
        return "Normal"


# -----------------------------
# MAIN LOOP
# -----------------------------
for participant in participants:

    folder_path = os.path.join(data_dir, participant)

    if not os.path.isdir(folder_path):
        continue

    print("Processing:", participant)

    # read signals
    thorac_time, thorac_value = thorac_values(folder_path)
    datetime, flow_values = values(folder_path)

    flow_values = np.array(flow_values, dtype=float)
    thorac_value = np.array(thorac_value, dtype=float)

    # bandpass filtering
    flow_filtered = bandpass_filter(flow_values, 0.17, 0.4, 32)
    thoracic_filtered = bandpass_filter(thorac_value, 0.17, 0.4, 32)

    
    def load_events(folder_path):

        file_path = os.path.join(folder_path, "flow_event.txt")

        events = []

        with open(file_path, "r") as f:

            lines = f.readlines()[5:]   # skip header

            for line in lines:

                line = line.strip()

                parts = line.split(";")

                time_range = parts[0]
                event_type = parts[2].strip()

                start_str, end_str = time_range.split("-")

                start_time = pd.to_datetime(start_str, format="%d.%m.%Y %H:%M:%S,%f")
                end_time = pd.to_datetime(end_str, format="%H:%M:%S,%f")

                end_time = start_time.replace(
                    hour=end_time.hour,
                    minute=end_time.minute,
                    second=end_time.second,
                    microsecond=end_time.microsecond
                )

                events.append({
                    "start_time": start_time,
                    "end_time": end_time,
                    "event": event_type
                })

        return pd.DataFrame(events)

    fs = 32

    windows = create_windows(flow_filtered, thoracic_filtered)

    events_df = load_events(folder_path)

    for window, start, end in windows:

        window_start = pd.to_datetime(datetime[start])
        window_end = pd.to_datetime(datetime[end])

        label = label_window(window_start, window_end, events_df)

        dataset_rows.append({
            "participant": participant,
            "window": window,
            "label": label
        })

       



# -----------------------------
# SAVE DATASET
# -----------------------------
dataset_df = pd.DataFrame(dataset_rows)

os.makedirs(out_dir, exist_ok=True)

output_path = os.path.join(out_dir, "breathing_dataset.pkl")

dataset_df.to_pickle(output_path)

print("Dataset saved at:", output_path)