import os
import argparse
import numpy as np
import pandas as pd
import pickle
from scipy.signal import butter, filtfilt

from vis_flow import vis_flow
from vis_thorac import thorac
from vis_spo2 import vis_spo2


# ------------------------
# Bandpass filter
# ------------------------
def bandpass_filter(signal, fs, low=0.17, high=0.4, order=4):

    nyq = 0.5 * fs
    low = low / nyq
    high = high / nyq

    b, a = butter(order, [low, high], btype='band')

    return filtfilt(b, a, signal)


# ------------------------
# Window creation
# ------------------------
def create_windows(signal, window_size, step):

    windows = []

    for i in range(0, len(signal) - window_size, step):

        windows.append(signal[i:i+window_size])

    return windows


# ------------------------
# Main
# ------------------------
parser = argparse.ArgumentParser()
parser.add_argument("-in_dir", required=True)
parser.add_argument("-out_dir", required=True)

args = parser.parse_args()

data_dir = args.in_dir
out_dir = args.out_dir

os.makedirs(out_dir, exist_ok=True)

dataset = []


participants = os.listdir(data_dir)

for p in participants:

    folder = os.path.join(data_dir, p)

    print("Processing:", p)

    # load signals
    t_flow, flow_values = vis_flow(folder, "flow.txt")
    t_thorac, thorac_values = thorac(folder, "thorac.txt")
    t_spo2, spo2_values = vis_spo2(folder, "spo2.txt")


    flow_values = np.array(flow_values)
    thorac_values = np.array(thorac_values)
    spo2_values = np.array(spo2_values)


    # filter breathing signals
    flow_values = bandpass_filter(flow_values, 32)
    thorac_values = bandpass_filter(thorac_values, 32)


    # window settings
    window_sec = 30
    overlap = 0.5

    flow_window = 32 * window_sec
    thorac_window = 32 * window_sec
    spo2_window = 4 * window_sec

    step_flow = int(flow_window * (1 - overlap))
    step_thorac = int(thorac_window * (1 - overlap))
    step_spo2 = int(spo2_window * (1 - overlap))


    flow_windows = create_windows(flow_values, flow_window, step_flow)
    thorac_windows = create_windows(thorac_values, thorac_window, step_thorac)
    spo2_windows = create_windows(spo2_values, spo2_window, step_spo2)


    n = min(len(flow_windows), len(thorac_windows), len(spo2_windows))


    for i in range(n):

        feature = np.concatenate([
            flow_windows[i],
            thorac_windows[i],
            spo2_windows[i]
        ])

        label = "Normal"

        dataset.append({
            "participant": p,
            "features": feature,
            "label": label
        })


# convert to dataframe
df = pd.DataFrame(dataset)


output_path = os.path.join(out_dir, "breathing_dataset.pkl")

with open(output_path, "wb") as f:
    pickle.dump(df, f)


print("Dataset saved:", output_path)

# import pandas as pd
# import numpy as np
# import os
# from scipy.signal import butter, filtfilt


# # -------------------------------
# # Bandpass Filter
# # -------------------------------
# def bandpass_filter(signal, lowcut, highcut, fs, order=4):

#     signal = np.array(signal)

#     nyquist = 0.5 * fs
#     low = lowcut / nyquist
#     high = highcut / nyquist

#     b, a = butter(order, [low, high], btype='band')

#     filtered_signal = filtfilt(b, a, signal)

#     return filtered_signal


# # -------------------------------
# # Preprocess signals
# # -------------------------------
# def preprocess_signals(airflow, thoracic):

#     airflow = bandpass_filter(
#         airflow,
#         0.17,
#         0.4,
#         fs=32
#     )

#     thoracic = bandpass_filter(
#         thoracic,
#         0.17,
#         0.4,
#         fs=32
#     )

#     return airflow, thoracic


# # -------------------------------
# # Window creation
# # -------------------------------
# def create_windows(signal, fs, window_sec=30, overlap=0.5):

#     window_size = int(window_sec * fs)
#     step = int(window_size * overlap)

#     windows = []

#     for start in range(0, len(signal) - window_size, step):

#         end = start + window_size
#         windows.append(signal[start:end])

#     return windows


# # -------------------------------
# # Label windows
# # -------------------------------
# def label_window(start, end, Disease, event_start_seconds, event_end_seconds):

#     for i in range(len(Disease)):

#         event_start = event_start_seconds[i]
#         event_end = event_end_seconds[i]

#         overlap = max(0, min(end, event_end) - max(start, event_start))

#         window_len = end - start

#         if overlap / window_len > 0.5:
#             return Disease[i]

#     return "Normal"


# # -------------------------------
# # Process one participant
# # -------------------------------
# def process_participant(folder_path):

#     airflow = pd.read_csv(folder_path+"/flow.txt",skiprows=7,sep=";",header=None,engine="python")
#     thoracic = pd.read_csv(folder_path+"/thorac.txt",skiprows=7,sep=";",header=None,engine="python")
#     spo2 = pd.read_csv(folder_path+"/spo2.txt",skiprows=7,sep=";",header=None,engine="python")
#     events = pd.read_csv(folder_path + "/flow_event.txt",skiprows=5,sep=";",header=None,engine="python")

#     flow_values = airflow.iloc[:,1].astype(float).values
#     thoracic_values = thoracic.iloc[:,1].astype(float).values
#     spo2_values = spo2.iloc[:,1].astype(float).values

#     Disease = events["event"].tolist()

#     start_timing = pd.to_datetime(events["start_time"])
#     end_timing = pd.to_datetime(events["end_time"])

#     reference_time = start_timing.iloc[0]

#     event_start_seconds = []
#     event_end_seconds = []

#     for i in range(len(Disease)):

#         event_start_seconds.append(
#             (start_timing.iloc[i] - reference_time).total_seconds()
#         )

#         event_end_seconds.append(
#             (end_timing.iloc[i] - reference_time).total_seconds()
#         )

#     airflow = np.array(flow_values)
#     thoracic = np.array(thoracic_values)
#     spo2 = np.array(spo2_values)

#     airflow, thoracic = preprocess_signals(airflow, thoracic)

#     airflow_windows = create_windows(airflow, fs=32)
#     thoracic_windows = create_windows(thoracic, fs=32)
#     spo2_windows = create_windows(spo2, fs=4)

#     labels = []

#     for i in range(len(airflow_windows)):

#         start_time = i * 15
#         end_time = start_time + 30

#         label = label_window(
#             start_time,
#             end_time,
#             Disease,
#             event_start_seconds,
#             event_end_seconds
#         )

#         labels.append(label)

#     min_len = min(
#         len(airflow_windows),
#         len(thoracic_windows),
#         len(spo2_windows)
#     )

#     dataset = []

#     for i in range(min_len):

#         row = {
#             "airflow": airflow_windows[i],
#             "thoracic": thoracic_windows[i],
#             "spo2": spo2_windows[i],
#             "label": labels[i]
#         }

#         dataset.append(row)

#     return dataset


# # -------------------------------
# # MAIN PIPELINE
# # -------------------------------
# DATA_DIR = "Data"

# all_data = []

# for participant in os.listdir(DATA_DIR):

#     folder = os.path.join(DATA_DIR, participant)

#     if os.path.isdir(folder):

#         print("Processing:", participant)

#         participant_data = process_participant(folder)

#         all_data.extend(participant_data)


# df = pd.DataFrame(all_data)

# os.makedirs("Dataset", exist_ok=True)

# df.to_pickle("Dataset/breathing_dataset.pkl")

# print("Dataset created successfully")