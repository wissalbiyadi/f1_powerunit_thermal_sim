import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import ttk
import threading
import time

from core.sensor_sim import simulate_temperature, simulate_temperature_secondary
from core.control_logic import determine_state
from core.logger import init_log, log_data
from config import constants


class CoolingSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏎️ F1 Power Unit Cooling Dashboard")
        self.root.geometry("360x360")  # Fixed window size

        # Optional: custom icon (put f1_icon.ico in ui/)
        # self.root.iconbitmap("ui/f1_icon.ico")

        self.running = False
        self.manual_fault = False

        # State variables
        self.temp = constants.TEMP_START
        self.state = "IDLE"
        self.fault_start_time = None
        self.fan_power = 0.0
        self.energy_used = 0.0
        self.start_time = None

        # === Fonts & Styles ===
        self.font_large = ("Segoe UI", 18, "bold")
        self.font_medium = ("Segoe UI", 14)

        # === UI Elements ===
        self.status_label = ttk.Label(root, text="System: IDLE", font=self.font_large, foreground="black")
        self.status_label.pack(pady=15)

        self.temp_label = ttk.Label(root, text="Temperature: -- °C", font=self.font_medium)
        self.temp_label.pack(pady=5)

        self.fan_label = ttk.Label(root, text="Fan Power: 0.0", font=self.font_medium)
        self.fan_label.pack(pady=5)

        self.energy_label = ttk.Label(root, text="Energy Used: 0.0 J", font=self.font_medium)
        self.energy_label.pack(pady=5)

        # Buttons
        self.start_btn = ttk.Button(root, text="▶ Start Simulation", command=self.start_simulation)
        self.start_btn.pack(pady=10)

        self.fault_btn = ttk.Button(root, text="💥 Inject Fault", command=self.toggle_fault)
        self.fault_btn.pack(pady=5)

        self.stop_btn = ttk.Button(root, text="⏹ Stop Simulation", command=self.stop_simulation, state=tk.DISABLED)
        self.stop_btn.pack(pady=10)

    def toggle_fault(self):
        self.manual_fault = not self.manual_fault
        self.fault_btn.config(text="✅ Fault Injected" if self.manual_fault else "💥 Inject Fault")

    def start_simulation(self):
        self.running = True
        self.start_time = time.time()
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        init_log()
        threading.Thread(target=self.simulation_loop, daemon=True).start()

    def stop_simulation(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def simulation_loop(self):
        while self.running:
            timestamp = time.time() - self.start_time

            # Fan logic
            if self.state == "COOLING":
                self.fan_power = min(1.0, self.fan_power + constants.FAN_RAMP_RATE * constants.UPDATE_INTERVAL)
            else:
                self.fan_power = max(0.0, self.fan_power - constants.FAN_COOLDOWN_RATE * constants.UPDATE_INTERVAL)

            self.energy_used += self.fan_power * constants.FAN_POWER_WATTS * constants.UPDATE_INTERVAL

            # Simulate sensor readings
            temp_primary = simulate_temperature(self.temp, self.state, self.fan_power)
            temp_secondary = simulate_temperature_secondary(self.temp, self.state, self.fan_power)
            sensor_diff = abs(temp_primary - temp_secondary)
            sensor_fault = sensor_diff > constants.SENSOR_TOLERANCE or self.manual_fault

            # Fault state tracking
            if sensor_fault and self.state != "FAULT":
                self.state = "FAULT"
                self.fault_start_time = timestamp

            # Average temps for logic
            self.temp = (temp_primary + temp_secondary) / 2

            self.state, self.fault_start_time = determine_state(
                self.temp, self.state, self.fault_start_time, timestamp, sensor_fault
            )

            # Log data
            log_data(timestamp, temp_primary, temp_secondary, self.fan_power, self.state)

            # Update UI
            self.update_ui()

            time.sleep(constants.UPDATE_INTERVAL)

    def update_ui(self):
        self.temp_label.config(text=f"Temperature: {round(self.temp, 2)} °C")
        self.fan_label.config(text=f"Fan Power: {round(self.fan_power, 2)}")
        self.energy_label.config(text=f"Energy Used: {round(self.energy_used, 1)} J")

        # Color-coded status
        state_colors = {
            "IDLE": "gray",
            "COOLING": "blue",
            "FAULT": "red",
            "SHUTDOWN": "black",
            "WARNING": "orange"
        }
        self.status_label.config(
            text=f"System: {self.state}",
            foreground=state_colors.get(self.state, "black")
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = CoolingSimulatorGUI(root)
    root.mainloop()
