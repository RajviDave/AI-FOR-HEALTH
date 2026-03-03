import matplotlib.pyplot as plt
from vis_flow import t_flow, rms_values
from vis_thorac import t_thorac, mean_values
from vis_spo2 import t_spo2, median_value
import numpy as np

# Convert to numpy arrays
t_flow = np.array(t_flow)
t_thorac = np.array(t_thorac)
t_spo2 = np.array(t_spo2)

airflow = np.array(rms_values)
thoracic = np.array(mean_values)
spo2 = np.array(median_value)

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

# Only interpolate if SpO2 has data
if len(t_spo2_trim) > 1 and len(t_air_trim) > 1:
    t_air_sec = np.array([(t - start_time).total_seconds() for t in t_air_trim])
    t_spo2_sec = np.array([(t - start_time).total_seconds() for t in t_spo2_trim])
    spo2_resampled = np.interp(t_air_sec, t_spo2_sec, spo2_trim)
else:
    spo2_resampled = []

# Plot
fig, axes = plt.subplots(3, 1, figsize=(15, 8), sharex=True)

axes[0].plot(t_air_trim, airflow_trim)
axes[0].set_ylabel("Airflow")

axes[1].plot(t_th_trim, thoracic_trim)
axes[1].set_ylabel("Thoracic")

if len(spo2_resampled) > 0:
    axes[2].plot(t_air_trim, spo2_resampled)
else:
    axes[2].plot(t_spo2_trim, spo2_trim)

axes[2].set_ylabel("SpO2")

plt.tight_layout()
plt.show()