import argparse
import os
import matplotlib.pyplot as plt

from vis_flow import vis_flow
from vis_thorac import thorac
from vis_spo2 import vis_spo2
from vis_eventflow import vis_eventflow


# command line argument
parser = argparse.ArgumentParser()
parser.add_argument("-name", required=True, help="Participant folder")

args = parser.parse_args()

folder = args.name
participant = os.path.basename(folder)


# get processed signals
t_flow, flow_values = vis_flow(folder,"flow.txt")
t_thorac, thorac_values = thorac(folder,"thorac.txt")
t_spo2, spo2_values = vis_spo2(folder,"spo2.txt")

# events = vis_eventflow(folder)


# create stacked plots
fig, axes = plt.subplots(3, 1, figsize=(15,10), sharex=True)


# airflow
axes[0].plot(t_flow, flow_values)
axes[0].set_title("Nasal Airflow")


# thoracic movement
axes[1].plot(t_thorac, thorac_values)
axes[1].set_title("Thoracic Movement")


# spo2
axes[2].plot(t_spo2, spo2_values)
axes[2].set_title("SpO2")


# overlay events
# for event in events:

#     start = event["start"]
#     end = event["end"]

#     for ax in axes:
#         ax.axvspan(start, end, alpha=0.3)


# plt.xlabel("Time")


# create output folder
os.makedirs("Visualizations", exist_ok=True)

output_path = f"Visualizations/{participant}_visualization.pdf"

plt.savefig(output_path)

print("Saved:", output_path)