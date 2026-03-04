import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages

from vis_flow import t_flow, rms_values
from vis_thorac import t_thorac, mean_values
from vis_spo2 import t_spo2, median_values

# create visualization folder
os.makedirs("visualizations", exist_ok=True)

pdf_path = "visualizations/signals.pdf"


# get global start and end time
start_time = min(t_flow[0], t_thorac[0], t_spo2[0])
end_time = max(t_flow[-1], t_thorac[-1], t_spo2[-1])


window = 45


with PdfPages(pdf_path) as pdf:

    current = start_time

    while current < end_time:

        next_time = current + np.timedelta64(window, 's')

        fig, ax = plt.subplots(3,1,sharex=True, figsize=(16,6))

        # FLOW
        flow_mask = [(current <= t < next_time) for t in t_flow]
        ax[0].plot(np.array(t_flow)[flow_mask], np.array(rms_values)[flow_mask])
        ax[0].set_title("Flow")
        ax[0].grid(True)

        # THORAC
        thorac_mask = [(current <= t < next_time) for t in t_thorac]
        ax[1].plot(np.array(t_thorac)[thorac_mask], np.array(mean_values)[thorac_mask])
        ax[1].set_title("Thorac")
        ax[1].grid(True)

        # SPO2
        spo2_mask = [(current <= t < next_time) for t in t_spo2]
        ax[2].plot(np.array(t_spo2)[spo2_mask], np.array(median_values)[spo2_mask])
        ax[2].set_title("SpO2")
        ax[2].grid(True)

        # format time axis
        ax[2].xaxis.set_major_locator(mdates.SecondLocator(interval=5))
        ax[2].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

        plt.xticks(rotation=90)
        plt.tight_layout()

        pdf.savefig(fig)
        plt.close(fig)

        current = next_time