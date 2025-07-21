from flask import Flask, jsonify
import threading
import monitor_logic  # Your gaze detection logic

app = Flask(__name__)
recording_thread = None

@app.route('/')
def home():
    return jsonify({'message': 'Avian Gaze API is running!'})

@app.route('/start_monitoring', methods=['GET'])
def start_monitoring():
    global recording_thread
    if recording_thread and recording_thread.is_alive():
        return jsonify({'status': 'already running'})

    recording_thread = threading.Thread(target=monitor_logic.start_recording)
    recording_thread.start()
    return jsonify({'status': 'monitoring started'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
