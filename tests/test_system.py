import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# tests/test_system.py

from core.control_logic import determine_state
from config import constants

print("=== Running All System Tests ===\n")


def test_fault_to_idle_recovery():
    print("▶️ Test: FAULT ➜ IDLE Recovery")
    state = "FAULT"
    temp = constants.COOLING_THRESHOLD - 2  # Low enough to recover to IDLE
    fault_start_time = 0.0
    timestamp = constants.FAULT_COOLDOWN + 1  # Ensure cooldown has passed
    new_state, _ = determine_state(temp, state, fault_start_time, timestamp, sensor_fault=False)
    assert new_state == "IDLE"
    print("✅ Passed")



def test_fault_escalates_to_shutdown():
    print("▶️ Test: FAULT ➜ SHUTDOWN")
    state = "FAULT"
    temp = constants.COOLING_THRESHOLD - 1
    timestamp = constants.FAULT_SHUTDOWN_TIME + 1
    fault_start_time = 0.0
    new_state, _ = determine_state(temp, state, fault_start_time, timestamp, sensor_fault=False)
    assert new_state == "SHUTDOWN"
    print("✅ Passed")


def test_idle_remains_idle_if_low_temp():
    print("▶️ Test: IDLE ➜ Remains IDLE if temp low and no fault")
    state = "IDLE"
    temp = constants.COOLING_THRESHOLD - 2
    new_state, _ = determine_state(temp, state, None, 10.0, sensor_fault=False)
    assert new_state == "IDLE"
    print("✅ Passed")


def test_warning_state():
    print("▶️ Test: Enters WARNING between thresholds")
    state = "COOLING"
    temp = (constants.WARNING_THRESHOLD + constants.FAULT_THRESHOLD) / 2  # Midpoint between thresholds
    fault_start_time = 0.0
    timestamp = 100.0  # Long enough to be outside FAULT handling
    sensor_fault = False

    new_state, _ = determine_state(temp, state, fault_start_time, timestamp, sensor_fault)
    
    # ✅ Make the test stronger
    assert new_state == "WARNING"
    assert new_state != "SHUTDOWN"  # 🔒 Ensures we didn’t escalate by mistake

    print("✅ Passed")


def test_fault_triggered_by_temp():
    print("▶️ Test: Triggers FAULT if temp exceeds fault threshold")

    state = "IDLE"
    temp = constants.FAULT_THRESHOLD + 5  # e.g., 100°C
    timestamp = 15.0
    sensor_fault = False

    new_state, fault_start = determine_state(temp, state, None, timestamp, sensor_fault)

    # 💡 Add debug output in case of failure
    if new_state != "FAULT":
        print(f"❌ Expected FAULT but got: {new_state}")
        print(f"   → Temp: {temp}, State: {state}, Sensor Fault: {sensor_fault}")

    assert new_state == "FAULT", f"Expected FAULT, got {new_state}"
    assert fault_start == timestamp, f"Expected fault_start to be {timestamp}, got {fault_start}"
    print("✅ Passed")




def test_sensor_fault_overrides_state():
    print("▶️ Test: Sensor Fault forces FAULT state")
    state = "IDLE"
    temp = constants.COOLING_THRESHOLD - 2
    timestamp = 5.0
    new_state, fault_start = determine_state(temp, state, None, timestamp, sensor_fault=True)
    assert new_state == "FAULT"
    assert fault_start == timestamp
    print("✅ Passed")


# === Run All Tests ===

test_fault_to_idle_recovery()
test_fault_escalates_to_shutdown()
test_idle_remains_idle_if_low_temp()
test_warning_state()
test_fault_triggered_by_temp()
test_sensor_fault_overrides_state()

print("\n🎉 ALL TESTS PASSED SUCCESSFULLY\n")
