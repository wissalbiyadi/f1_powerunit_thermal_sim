import matplotlib.pyplot as plt
from config import constants

def setup_plot():
    plt.ion()  # Turn on interactive mode

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()  # Secondary y-axis for fan power

    # Configure primary axis (Temperature)
    ax1.set_title("F1 Power Unit Cooling System Simulation")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Temperature (°C)", color="blue")
    ax1.set_ylim(50, 100)
    ax1.grid(True)

    # Plot threshold lines (only once)
    ax1.axhline(constants.COOLING_THRESHOLD, color='green', linestyle='--', label='Cooling Start')
    ax1.axhline(constants.WARNING_THRESHOLD, color='orange', linestyle='--', label='Warning')
    ax1.axhline(constants.FAULT_THRESHOLD, color='red', linestyle='--', label='Critical')

    # Configure secondary axis (Fan Power)
    ax2.set_ylabel("Fan Power (0–1)", color="purple")
    ax2.set_ylim(0, 1)

    return fig, ax1, ax2

def update_plot(ax1, ax2, timestamps, temps, fan_powers):
    ax1.cla()
    ax2.cla()

    # Redraw threshold lines (since we cleared)
    ax1.axhline(constants.COOLING_THRESHOLD, color='green', linestyle='--', label='Cooling Start')
    ax1.axhline(constants.WARNING_THRESHOLD, color='orange', linestyle='--', label='Warning')
    ax1.axhline(constants.FAULT_THRESHOLD, color='red', linestyle='--', label='Critical')

    # Plot main temperature line
    ax1.plot(timestamps, temps, label="Temperature (°C)", color="blue")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Temperature (°C)", color="blue")
    ax1.set_ylim(50, 100)

    # Plot fan power line
    ax2.plot(timestamps, fan_powers, label="Fan Power (PWM)", color="purple", linestyle="--")
    ax2.set_ylabel("Fan Power (0–1)", color="purple")
    ax2.set_ylim(0, 1)

    # Combine legends from both axes
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    plt.pause(0.05)
