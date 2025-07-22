from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/start-monitoring', methods=['POST'])
def start_monitoring():
    try:
        subprocess.Popen(["python3", "start_script.py"])
        return jsonify({'message': 'Monitoring started successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Avian Gaze Monitoring API is running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
