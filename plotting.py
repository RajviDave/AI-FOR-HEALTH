import matplotlib.pyplot as plt
from vis_flow import final_time,rms_values
from vis_thorac import mean_values
from vis_spo2 import median_value
import pandas as pd

fig, axes = plt.subplots(2, 1, figsize=(18, 8), sharex=True)


# Nasal Airflow
axes[0].plot(final_time, rms_values, color='blue')
axes[0].set_ylabel("Nasal Flow (a.u)")
axes[0].set_title("AP_01 - Example Segment")

# Thoracic Movement
axes[1].plot(final_time, mean_values, color='orange')
axes[1].set_ylabel("Resp. Amplitude")

# axes[2].plot(final_time, median_value, color='gray')
# axes[2].set_ylabel("SpO2 (%)")
# axes[2].set_xlabel("Time")

# make time index

plt.tight_layout()
plt.show()
# plt.figure(figsize=(10,5))

# plt.plot(final_time[:200], rms_values[:200], marker='o')

# plt.xlabel("Time")
# plt.ylabel("RMS Value")
# plt.title("First 30 Seconds RMS")

# plt.xticks(rotation=45)

# plt.tight_layout()
# plt.show()


# plt.figure(figsize=(10,5))

# plt.plot(final_time[:200], mean_values[:200], marker='o')

# plt.xlabel("Time")
# plt.ylabel("Mean Value")
# plt.title("First 30 Seconds RMS")

# plt.xticks(rotation=45)

# plt.tight_layout()
# plt.show()

# plt.figure(figsize=(10,5))

# plt.plot(final_time[:200], median_value[:200], marker='o')

# plt.xlabel("Time")
# plt.ylabel("Median Value")
# plt.title("First 30 Seconds Mean")

# plt.xticks(rotation=45)

# plt.tight_layout()
# plt.show()