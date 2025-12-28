from flask import Flask, jsonify
import json

app = Flask(__name__)

DATA_FILE = "data.json"

# -----------------------------
# Get latest vitals
# -----------------------------
@app.route("/latest", methods=["GET"])
def get_latest():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            if len(data) == 0:
                return jsonify({"message": "No data available"})
            return jsonify(data[-1])
    except:
        return jsonify({"error": "Data file not found"}), 500


# -----------------------------
# Get all vitals (history)
# -----------------------------
@app.route("/history", methods=["GET"])
def get_history():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return jsonify(data)
    except:
        return jsonify({"error": "Data file not found"}), 500


if __name__ == "__main__":
    app.run(debug=True)
