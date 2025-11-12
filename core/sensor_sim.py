import random
from config import constants

def simulate_temperature(prev_temp, state, fan_power):
    """Simulate temperature sensor based on system state"""

    # Random drift to simulate noise
    drift = random.uniform(-0.2, 0.2)

    if state == "COOLING":
        # Cooling effect scaled by fan power
        delta = -fan_power * constants.MAX_COOLING_RATE
    elif state == "FAULT":
        # Sensor stuck or climbing aggressively
        delta = random.uniform(0.2, 0.6)
    else:
        # Normal heating (e.g. engine warming)
        delta = random.uniform(0.1, 0.5)

    return prev_temp + delta + drift


def simulate_temperature_secondary(prev_temp, state, fan_power):
    """Second redundant sensor with a bit more noise"""
    base = simulate_temperature(prev_temp, state, fan_power)
    noise = random.uniform(-0.3, 0.3)
    return base + noise
