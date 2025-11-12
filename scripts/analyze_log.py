import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import csv
from collections import defaultdict
from config import constants


LOG_PATH = "data/log.csv"

def score_simulation(max_temp, avg_fan, energy_used, state_durations):
    """Calculate a performance score based on thermal and energy efficiency."""
    score = 100

    # Penalize high max temperature
    if max_temp > constants.FAULT_THRESHOLD:
        score -= 30
    elif max_temp > constants.WARNING_THRESHOLD:
        score -= 10

    # Penalize high energy usage
    if energy_used > 500:
        score -= 20
    elif energy_used > 250:
        score -= 10

    # Penalize long fault duration
    fault_time = state_durations.get("FAULT", 0)
    if fault_time > 15:
        score -= 20
    elif fault_time > 5:
        score -= 10

    return max(0, round(score))  # Ensure score doesn't go below 0


def analyze_log(filepath):
    """Analyze the simulation log and print key metrics and efficiency score."""
    if not os.path.exists(filepath):
        print("❌ Log file not found. Run simulation first.")
        return

    timestamps = []
    fan_powers = []
    temps = []
    states = []

    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            timestamps.append(float(row[0]))
            temps.append(float(row[1]))
            fan_powers.append(float(row[3]))
            states.append(row[4] if len(row) > 4 else "UNKNOWN")

    # Basic stats
    duration = timestamps[-1] - timestamps[0]
    max_temp = max(temps)
    avg_fan_power = sum(fan_powers) / len(fan_powers)
    total_energy = sum(fp * constants.FAN_POWER_WATTS * constants.UPDATE_INTERVAL for fp in fan_powers)

    # Time spent in each state
    state_time = defaultdict(float)
    for i in range(1, len(timestamps)):
        delta = timestamps[i] - timestamps[i - 1]
        state_time[states[i]] += delta

    # === Output Analysis ===
    print("\n=== 📊 Post-Run Analysis ===")
    print(f"🔺 Max Temperature: {round(max_temp, 2)}°C")
    print(f"🧊 Avg Fan Power: {round(avg_fan_power, 2)} (0–1 scale)")
    print(f"⚡ Total Energy Used: {round(total_energy, 2)} J")
    print(f"⏱️ Total Simulation Time: {round(duration, 2)} s")
    print("⌛ State Durations:")
    for state, time_spent in state_time.items():
        print(f"   - {state}: {round(time_spent, 2)} s")

    # Efficiency Score
    score = score_simulation(max_temp, avg_fan_power, total_energy, state_time)
    print(f"\n🏁 Efficiency Score: {score}/100")
    print("===========================\n")


if __name__ == "__main__":
    analyze_log(LOG_PATH)
