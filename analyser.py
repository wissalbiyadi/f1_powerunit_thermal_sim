import pandas as pd
import matplotlib.pyplot as plt
from config import constants

# Load the data
log = pd.read_csv(constants.LOG_PATH, encoding="cp1252")

# Extract values
time = log["Time (s)"]
temp1 = log["Temp Sensor 1 (°C)"]
temp2 = log["Temp Sensor 2 (°C)"]
state = log["State"]

# Create FAULT mask
fault_mask = state == "FAULT"

# Plot temps
plt.figure(figsize=(12, 6))
plt.plot(time, temp1, label="Sensor 1", color='blue')
plt.plot(time, temp2, label="Sensor 2", color='cyan')
plt.fill_between(time, 20, 100, where=fault_mask, color='red', alpha=0.1, label="FAULT Period")

# Draw state thresholds
plt.axhline(constants.COOLING_THRESHOLD, color='green', linestyle='--', label='Cooling Start')
plt.axhline(constants.WARNING_THRESHOLD, color='orange', linestyle='--', label='Warning')
plt.axhline(constants.FAULT_THRESHOLD, color='red', linestyle='--', label='Critical')

# Labels
plt.title("Post-Run Analysis: F1 PU Thermal Control")
plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()