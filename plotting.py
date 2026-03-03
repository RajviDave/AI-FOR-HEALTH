import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from vis_flow import t_flow, rms_values
from vis_thorac import t_thorac, mean_values
from vis_spo2 import t_spo2, median_value
from vis_eventflow import start_timing, end_timing, Disease
import numpy as np

# Convert to numpy arrays
t_flow = np.array(t_flow)
t_thorac = np.array(t_thorac)
t_spo2 = np.array(t_spo2)

airflow = np.array(rms_values)
thoracic = np.array(mean_values)
spo2 = np.array(median_value)

start_timing = np.array(start_timing)
end_timing = np.array(end_timing)
Disease = np.array(Disease)

# Find overlapping time range
start_time = max(t_flow[0], t_thorac[0], t_spo2[0])
end_time = min(t_flow[-1], t_thorac[-1], t_spo2[-1])

# Trim airflow
mask_air = (t_flow >= start_time) & (t_flow <= end_time)
t_air_trim = t_flow[mask_air]
airflow_trim = airflow[mask_air]

# Trim thoracic
mask_th = (t_thorac >= start_time) & (t_thorac <= end_time)
t_th_trim = t_thorac[mask_th]
thoracic_trim = thoracic[mask_th]

# Trim SpO2
mask_spo2 = (t_spo2 >= start_time) & (t_spo2 <= end_time)
t_spo2_trim = t_spo2[mask_spo2]
spo2_trim = spo2[mask_spo2]

# Interpolate SpO2
if len(t_spo2_trim) > 1 and len(t_air_trim) > 1:
    t_air_sec = np.array([(t - start_time).total_seconds() for t in t_air_trim])
    t_spo2_sec = np.array([(t - start_time).total_seconds() for t in t_spo2_trim])
    spo2_resampled = np.interp(t_air_sec, t_spo2_sec, spo2_trim)
else:
    spo2_resampled = np.zeros(len(t_air_trim))

# Downsample to 5-second interval
t_air_sec = np.array([(t - t_air_trim[0]).total_seconds() for t in t_air_trim])
indices_5s = np.where(t_air_sec % 5 < 0.1)[0]

t_5s = t_air_trim[indices_5s]
air_5s = airflow_trim[indices_5s]
thor_5s = thoracic_trim[indices_5s]
spo2_5s = spo2_resampled[indices_5s]

# Event colors
event_colors = {
    "Hypopnea": "yellow",
    "Obstructive Apnea": "red",
}

# Create folder
os.makedirs("Visualizations", exist_ok=True)
pdf_path = "Visualizations/sleep_visualization.pdf"

chunk_size = 45
total_points = len(t_5s)

with PdfPages(pdf_path) as pdf:
    for i in range(0, total_points, chunk_size):
        end = i + chunk_size

        fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

        # Plot signals
        axes[0].plot(t_5s[i:end], air_5s[i:end])
        axes[0].set_ylabel("Airflow")

        axes[1].plot(t_5s[i:end], thor_5s[i:end])
        axes[1].set_ylabel("Thoracic")

        axes[2].plot(t_5s[i:end], spo2_5s[i:end])
        axes[2].set_ylabel("SpO2")
        axes[2].set_xlabel("Time")

        # ---- Event Highlighting ----
        current_start = t_5s[i]
        current_end = t_5s[min(end-1, total_points-1)]

        for ev_start, ev_end, label in zip(start_timing, end_timing, Disease):

            # Only shade if event overlaps current chunk
            if ev_end >= current_start and ev_start <= current_end:

                color = event_colors.get(label, "gray")

                for ax in axes:
                    ax.axvspan(
                        max(ev_start, current_start),
                        min(ev_end, current_end),
                        color=color,
                        alpha=0.3
                    )

        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

print("PDF saved at:", pdf_path)