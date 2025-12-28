import random
import time
import json
from datetime import datetime

# -------------------------------
# SENSOR SIMULATION FUNCTIONS
# -------------------------------

def heart_rate_sensor():
    return random.randint(105, 115)

def spo2_sensor():
    return random.randint(92, 100)

def bp_sensor():
    return random.randint(100, 150)

def temperature_sensor():
    return round(random.uniform(38.5, 39.5), 1)

# -------------------------------
# GENERATE VITALS
# -------------------------------

def generate_vitals():
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "HR": heart_rate_sensor(),
        "SpO2": spo2_sensor(),
        "BP": bp_sensor(),
        "Temp": temperature_sensor()
    }

# -------------------------------
# ABNORMAL CHECK
# -------------------------------

def is_abnormal(v):
    return (
        v["HR"] < 60 or v["HR"] > 100 or
        v["SpO2"] < 94 or
        v["BP"] > 140 or
        v["Temp"] > 38
    )

# -------------------------------
# ALERT DECISION
# -------------------------------

def decide_alert(count):
    if count >= 8:
        return "RED"
    elif count >= 5:
        return "YELLOW"
    else:
        return "GREEN"

# -------------------------------
# SAFE JSON SAVE (FIXED)
# -------------------------------

def save_to_json(entry):
    file_name = "data.json"

    try:
        with open(file_name, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(entry)

    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------------
# MAIN LOOP
# -------------------------------

abnormal_count = 0

print("Backend started... Press Ctrl+C to stop.\n")

try:
    while True:
        vitals = generate_vitals()

        if is_abnormal(vitals):
            abnormal_count += 1
        else:
            abnormal_count = 0

        vitals["alert"] = decide_alert(abnormal_count)

        print(vitals)
        save_to_json(vitals)

        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram stopped safely. All data saved.")
