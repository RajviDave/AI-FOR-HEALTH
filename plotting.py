import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from matplotlib.backends.backend_pdf import PdfPages

from vis_flow import rms_values
from vis_thorac import mean_values
from vis_spo2 import median_values


# sampling rates
fs_flow = 32
fs_thorac = 32
fs_spo2 = 4


# reconstruct time in seconds
t_flow = np.arange(len(rms_values)) / fs_flow
t_thorac = np.arange(len(mean_values)) / fs_thorac
t_spo2 = np.arange(len(median_values)) / fs_spo2


# start timestamp
start_time = datetime.strptime("17 20:38:28", "%d %H:%M:%S")


# convert to datetime
time_flow = [start_time + timedelta(seconds=float(t)) for t in t_flow]
time_thorac = [start_time + timedelta(seconds=float(t)) for t in t_thorac]
time_spo2 = [start_time + timedelta(seconds=float(t)) for t in t_spo2]


# output folder
os.makedirs("visualizations", exist_ok=True)
pdf_path = "visualizations/signals.pdf"


# determine total duration
total_time = max(t_flow[-1], t_thorac[-1], t_spo2[-1])


with PdfPages(pdf_path) as pdf:

    # create windows of 5 seconds
    for start in np.arange(0, total_time, 5):

        end = start + 5

        fig, ax = plt.subplots(3,1,sharex=True, figsize=(12,6))

        # select window data
        flow_mask = (t_flow >= start) & (t_flow < end)
        thorac_mask = (t_thorac >= start) & (t_thorac < end)
        spo2_mask = (t_spo2 >= start) & (t_spo2 < end)

        ax[0].plot(np.array(time_flow)[flow_mask], np.array(rms_values)[flow_mask])
        ax[0].set_title("Flow")
        ax[0].grid(True)

        ax[1].plot(np.array(time_thorac)[thorac_mask], np.array(mean_values)[thorac_mask])
        ax[1].set_title("Thorac")
        ax[1].grid(True)

        ax[2].plot(np.array(time_spo2)[spo2_mask], np.array(median_values)[spo2_mask])
        ax[2].set_title("SpO2")
        ax[2].grid(True)

        # format x-axis time
        ax[2].xaxis.set_major_locator(mdates.SecondLocator(interval=5))
        ax[2].xaxis.set_major_formatter(mdates.DateFormatter("%d %H:%M:%S"))

        plt.xticks(rotation=90)
        plt.tight_layout()

        pdf.savefig(fig)
        plt.close(fig)