from config import constants

def determine_state(temp, current_state, fault_start_time, timestamp, sensor_fault):
    """Determine system state based on temp, sensor fault and fault duration"""

    # Sensor fault takes priority — trigger immediate FAULT
    if sensor_fault and current_state != "FAULT":
        return "FAULT", timestamp

    if current_state == "FAULT":
        # Time in fault state
        time_in_fault = timestamp - fault_start_time

        # 🚨 Safety escalation — force shutdown if fault lasts too long
        if time_in_fault >= constants.FAULT_SHUTDOWN_TIME:
            return "SHUTDOWN", None

        # ⏳ Still within cooldown period — remain in FAULT
        elif time_in_fault < constants.FAULT_COOLDOWN:
            return "FAULT", fault_start_time

        # ✅ Cooldown expired — try recovery based on temperature
        else:
            if temp >= constants.COOLING_THRESHOLD:
                return "COOLING", None
            else:
                return "IDLE", None


    # === Normal operation with hysteresis and safety ===

    # 🚨 Always prioritize thermal FAULT if temp is too high
    if temp >= constants.FAULT_THRESHOLD:
        return "FAULT", timestamp

    # Then check WARNING
    elif constants.WARNING_THRESHOLD <= temp < constants.FAULT_THRESHOLD:
        return "WARNING", None

    # Normal hysteresis
    elif current_state == "IDLE" and temp >= constants.COOLING_THRESHOLD:
        return "COOLING", None
    elif current_state == "COOLING" and temp <= constants.COOLING_THRESHOLD - 1.5:
        return "IDLE", None

    # Otherwise, stay in current state
    else:
        return current_state, None

