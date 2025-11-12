import time

from core.sensor_sim import simulate_temperature, simulate_temperature_secondary
from core.control_logic import determine_state
from core.logger import init_log, log_data
from visualisation.live_plot import setup_plot, update_plot
from config import constants
import matplotlib.pyplot as plt
import keyboard  # Listen for fault keypress

manual_fault = False

# Initialise components
init_log()
fig, ax1, ax2 = setup_plot()

# Variables to track simulation state
temps = []
states = []
timestamps = []

fan_powers = []  # Track fan power for plotting

# Starting temp and time
temp = constants.TEMP_START
start_time = time.time()

print("=== F1 Power Unit Cooling & Fault Simulation ===")

# Track current system state
state = "IDLE"
fault_start_time = None

fan_power = 0.0  # 0.0 = off, 1.0 = full power
energy_used = 0.0  # Joules (or kJ if scaled)


try:
    while True:
        # 1. Timestamp
        timestamp = time.time() - start_time

        # Toggle manual fault
        if keyboard.is_pressed('f'):
            manual_fault = True
        else:
            manual_fault = False

        # Update fan power based on state
        if state == "COOLING":
            fan_power = min(1.0, fan_power + constants.FAN_RAMP_RATE * constants.UPDATE_INTERVAL)
        else:
            fan_power = max(0.0, fan_power - constants.FAN_COOLDOWN_RATE * constants.UPDATE_INTERVAL)


        energy_used += fan_power * constants.FAN_POWER_WATTS * constants.UPDATE_INTERVAL  # Energy = Power × Time

        # Print energy usage every 10 seconds
        if int(timestamp) % 10 == 0 and int(timestamp) != 0:
            print(f"[Energy Usage] 🔋 Fan Energy Consumed: {round(energy_used, 2)} J")


        # 2. Simulate new temperature
        temp_primary = simulate_temperature(temp, state, fan_power)
        temp_secondary = simulate_temperature_secondary(temp, state, fan_power)

        # Sensor comparison fault
        if manual_fault:
            sensor_fault = True
            print(f"[{round(timestamp,1)}s] 🧪 Manual fault injected!")
        else:
            sensor_diff = abs(temp_primary - temp_secondary)
            sensor_fault = sensor_diff > constants.SENSOR_TOLERANCE


        # Use average for control logic
        temp = (temp_primary + temp_secondary) / 2

        if sensor_fault:
            state = "FAULT"
            if fault_start_time is None:
                fault_start_time = timestamp

        # 3. Determine new state
        state, fault_start_time = determine_state(
            temp, state, fault_start_time, timestamp, sensor_fault
        )

        # Handle system shutdown scenario
        if state == "SHUTDOWN":
            print(f"[{round(timestamp,1)}s] ❌ SYSTEM SHUTDOWN — Fault duration exceeded safety limit!")
            break  # Exit the simulation loop

        if state == "FAULT":
            print(f"[{round(timestamp,1)}s] ⚠️ FAULT ACTIVE — Cooling down ({round(timestamp - fault_start_time,1)}s)")

        # 4. Log
        log_data(timestamp, temp_primary, temp_secondary, fan_power, state)

        # 5. Track for plotting
        temps.append(temp)
        states.append(state)
        timestamps.append(timestamp)
        fan_powers.append(fan_power)

        # 6. Console output
        fan = "ON" if state == "COOLING" else "OFF"
        print(f"[{round(timestamp,1)}s] Temp: {round(temp,1)}°C | State: {state} | Fan Power: {round(fan_power,2)}")

        # 7. Update plot
        update_plot(ax1, ax2, timestamps, temps, fan_powers)

        # 8. Wait
        time.sleep(constants.UPDATE_INTERVAL)

except KeyboardInterrupt:
    plt.savefig("data/f1_cooling_sim_plot.png")  #Save plot
    print("\nSimulation ended by user. Log saved to data/log.csv")
