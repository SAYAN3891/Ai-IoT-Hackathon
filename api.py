# api.py
import time
import random
import firebase_admin
from firebase_admin import credentials, firestore

# -------------------------------
# STEP 1: Firebase Initialization
# -------------------------------
cred = credentials.Certificate("firebase_key.json")  # friend ka JSON file
firebase_admin.initialize_app(cred)

db = firestore.client()  # Firestore client

# -------------------------------
# STEP 2: Generate Vitals Function
# -------------------------------
def generate_vitals():
    """
    Generates random vitals data.
    You can enhance this with alert logic if needed.
    """
    hr = random.randint(60, 110)
    spo2 = random.randint(94, 100)
    bp = random.randint(100, 150)
    temp = round(random.uniform(36.5, 38.8), 1)
    
    # Simple alert logic
    if hr < 60 or hr > 100 or spo2 < 94 or bp < 90 or bp > 140 or temp < 36 or temp > 38:
        alert = "YELLOW"
    else:
        alert = "GREEN"
    
    vitals = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "HR": hr,
        "SpO2": spo2,
        "BP": bp,
        "Temp": temp,
        "alert": alert
    }
    return vitals

# -------------------------------
# STEP 3: Send to Firebase Function
# -------------------------------
def send_to_firebase(vitals):
    try:
        doc_ref = db.collection("vitals").document()  # Firestore collection 'vitals'
        doc_ref.set(vitals)
        print("✅ Sent to Firebase successfully")
    except Exception as e:
        print("❌ Firebase connection failed:", e)

# -------------------------------
# STEP 4: Main Loop
# -------------------------------
if __name__ == "__main__":
    print("Backend started... Press Ctrl+C to stop.")
    try:
        while True:
            vitals = generate_vitals()
            print(vitals)           # Local console me print
            send_to_firebase(vitals)  # Send to Firebase
            time.sleep(1)            # 1-second interval
    except KeyboardInterrupt:
        print("Program stopped safely.")
