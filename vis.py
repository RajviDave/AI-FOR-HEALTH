import argparse
import os
import matplotlib.pyplot as plt

from vis_flow import vis_flow
from vis_thorac import vis_thorac
from vis_spo2 import vis_spo2
from vis_eventflow import vis_eventflow


parser = argparse.ArgumentParser()
parser.add_argument("-name", required=True, help="Participant folder path")

args = parser.parse_args()

folder = args.name
participant = os.path.basename(folder)


# call your existing scripts
flow_time, flow_val = vis_flow(folder)
thor_time, thor_val = vis_thorac(folder)
spo2_time, spo2_val = vis_spo2(folder)
events = vis_eventflow(folder)


# create stacked plot
fig, axes = plt.subplots(3, 1, figsize=(15,10), sharex=True)


# Nasal airflow
axes[0].plot(flow_time, flow_val)
axes[0].set_title("Nasal Airflow")


# Thoracic movement
axes[1].plot(thor_time, thor_val)
axes[1].set_title("Thoracic Movement")


# SpO2
axes[2].plot(spo2_time, spo2_val)
axes[2].set_title("SpO2")


# overlay breathing events
for event in events:

    start = event["start"]
    end = event["end"]

    for ax in axes:
        ax.axvspan(start, end, alpha=0.3)


plt.xlabel("Time")


# create visualization folder
os.makedirs("Visualizations", exist_ok=True)

output = f"Visualizations/{participant}_visualization.pdf"

plt.savefig(output)

print("Visualization saved:", output)