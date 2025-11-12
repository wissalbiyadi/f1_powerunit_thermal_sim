import csv
import os

def init_log():
    """
    Initialise the CSV log file.
    Creates the 'data' folder if it doesn't exist, and writes column headers.
    """
    if not os.path.exists("data"):
        os.makedirs("data")  # Ensure directory exists before writing

    with open("data/log.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        # CSV header for analysis and debugging
        writer.writerow(["timestamp", "temp_primary", "temp_secondary", "fan_power", "state"])


def log_data(timestamp, temp_primary, temp_secondary, fan_power, state):
    """
    Append a new row of data to the log.

    Parameters:
    - timestamp: Time (seconds since simulation start)
    - temp_primary: Temperature from primary sensor
    - temp_secondary: Temperature from secondary sensor
    - fan_power: Current fan power (0.0 to 1.0)
    - state: Current system state (e.g., IDLE, COOLING, FAULT, SHUTDOWN)
    """
    with open("data/log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            round(timestamp, 1),
            round(temp_primary, 1),
            round(temp_secondary, 1),
            round(fan_power, 2),
            state
        ])
