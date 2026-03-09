import argparse
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from matplotlib.backends.backend_pdf import PdfPages

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

os.makedirs("Visualizations", exist_ok=True)
pdf_path = f"Visualizations/{participant}_visualization.pdf"

start_time = min(t_flow[0], t_thorac[0], t_spo2[0])
end_time = max(t_flow[-1], t_thorac[-1], t_spo2[-1])


window = 45   # seconds per page


with PdfPages(pdf_path) as pdf:

    current = start_time

    while current < end_time:

        next_time = current + timedelta(seconds=window)

        fig, ax = plt.subplots(3,1,sharex=True, figsize=(16,6))

        # FLOW
        flow_mask = [(current <= t < next_time) for t in t_flow]
        ax[0].plot(np.array(t_flow)[flow_mask], np.array(flow_values)[flow_mask])
        ax[0].set_ylabel("Nasal Flow (L/min)")
        ax[0].grid(True)

        # THORAC
        thorac_mask = [(current <= t < next_time) for t in t_thorac]
        ax[1].plot(np.array(t_thorac)[thorac_mask], np.array(thorac_values)[thorac_mask])
        ax[1].set_ylabel("Resp. Amplitude")
        ax[1].grid(True)

        # SPO2
        spo2_mask = [(current <= t < next_time) for t in t_spo2]
        ax[2].plot(np.array(t_spo2)[spo2_mask], np.array(spo2_values)[spo2_mask])
        ax[2].set_ylabel("SpO2 (%)")
        ax[2].grid(True)

        # timestamp ticks every 5 seconds
        ax[2].xaxis.set_major_locator(mdates.SecondLocator(interval=5))
        ax[2].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

        plt.xticks(rotation=90)
        plt.tight_layout()

        pdf.savefig(fig)
        plt.close(fig)

        current = next_time


print("Saved:", pdf_path)