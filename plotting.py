import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from vis_flow import t_flow, rms_values
from vis_thorac import t_thorac, mean_values
from vis_spo2 import t_spo2, median_values
from vis_eventflow import start_timing, end_timing, Disease
import numpy as np

# reconstruct time axis
t_flow = np.arange(len(rms_values)) / 32
t_thorac = np.arange(len(mean_values)) / 32
t_spo2 = np.arange(len(median_values)) / 4

# create subplot
fig, ax = plt.subplots(3, 1, sharex=True, figsize=(12,6))

ax[0].plot(t_flow, rms_values)
ax[0].set_title("Flow")

ax[1].plot(t_thorac, mean_values)
ax[1].set_title("Thorac")

ax[2].plot(t_spo2, median_values)
ax[2].set_title("SpO2")

ax[2].set_xlabel("Time (seconds)")

plt.tight_layout()
plt.show()