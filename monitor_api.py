from flask import Flask, jsonify
from monitor_logic import run_gaze_monitoring
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return "Avian Gaze Monitoring API is running"

@app.route('/start-monitoring', methods=['GET'])
def start_monitoring():
    thread = threading.Thread(target=run_gaze_monitoring)
    thread.start()
    return jsonify({"message": "Monitoring started in background"}), 200

if __name__ == '__main__':
    app.run(debug=True)
