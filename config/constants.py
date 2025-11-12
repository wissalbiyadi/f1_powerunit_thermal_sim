# Thresholds for system states (°C)
COOLING_THRESHOLD = 60
WARNING_THRESHOLD = 85
FAULT_THRESHOLD = 95

# Simulation settings
TEMP_START = 55.0
TEMP_DRIFT_RANGE = (-0.3, 0.6)  # min, max per update
UPDATE_INTERVAL = 0.5  # seconds between updates

# CSV log path
LOG_PATH = "data/log.csv"

FAULT_COOLDOWN = 10  # seconds to stay in FAULT before recovering

DRIFT_UP = 0.6         # max temp rise per loop (°C)
DRIFT_DOWN = 0.5       # max cooling per loop (°C)

SENSOR_TOLERANCE = 5.0  # Max °C allowed between sensors

FAULT_RECOVERY_TIME = 10.0  # seconds

FAN_RAMP_RATE = 0.5       # power units per second (e.g. from 0 to 1 in 2s)
FAN_COOLDOWN_RATE = 0.7   # faster decay when turning off
MAX_COOLING_RATE = 1.2    # max degrees C per second the fan can cool

FAN_POWER_WATTS = 50.0  # Example: 50 watts max
FAULT_SHUTDOWN_TIME = 20.0  # seconds in FAULT before shutdown
