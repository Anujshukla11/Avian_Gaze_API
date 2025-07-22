from flask import Flask, jsonify
import threading
from monitor_logic import run_gaze_monitoring  # Make sure your logic file is named monitor_logic.py

app = Flask(__name__)

monitoring_thread = None

@app.route('/')
def home():
    return "Avian Gaze Monitoring API is running."

@app.route('/start-monitoring', methods=['GET'])
def start_monitoring():
    global monitoring_thread
    if monitoring_thread and monitoring_thread.is_alive():
        return jsonify({"message": "Monitoring is already running."}), 200
    
    monitoring_thread = threading.Thread(target=run_gaze_monitoring, daemon=True)
    monitoring_thread.start()
    return jsonify({"message": "Monitoring started."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
