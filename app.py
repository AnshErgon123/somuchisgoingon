# app.py

from flask import Flask, render_template_string, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

message_count = 0
connected = False

# HTML UI
HTML_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ERGON - CAN Monitor</title>
  <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
  <style>
    body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; margin: 0; }
    header { background: #000; color: #fff; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
    header h1 { font-size: 24px; margin: 0; }
    header img { height: 40px; }
    .container { padding: 30px; max-width: 1000px; margin: auto; }
    .status { font-weight: bold; font-size: 18px; margin-bottom: 10px; }
    .connected { color: green; }
    .disconnected { color: red; }
    #total { margin-bottom: 20px; font-size: 16px; }
    table { width: 100%; border-collapse: collapse; background: white; }
    th, td { padding: 10px; border: 1px solid #ddd; text-align: center; }
    th { background: #003366; color: white; }
    tr:nth-child(odd) { background: #f9f9f9; }
    tr:hover { background: #e2f0ff; }
  </style>
</head>
<body>
  <header>
    <h1>ERGON - CAN Monitor</h1>
    <img src="{{ url_for('static', filename='download.png') }}" alt="ERGON Logo">
  </header>
  <div class="container">
    <div class="status">Status: <span id="status-text" class="disconnected">Disconnected</span></div>
    <div id="total">Total Messages: <span id="message-count">0</span></div>
    <table>
      <thead>
        <tr><th>Timestamp</th><th>ID</th><th>Data</th></tr>
      </thead>
      <tbody id="data-table"></tbody>
    </table>
  </div>
  <script>
    const socket = io();
    const statusText = document.getElementById('status-text');
    const countEl = document.getElementById('message-count');
    const tableBody = document.getElementById('data-table');
    let count = 0;

    function updateStatus(isConnected) {
      statusText.textContent = isConnected ? 'Connected' : 'Disconnected';
      statusText.className = isConnected ? 'connected' : 'disconnected';
    }

    fetch('/status').then(res => res.json()).then(data => updateStatus(data.connected));

    socket.on('can_message', msg => {
      const row = tableBody.insertRow(-1);
      row.insertCell(0).textContent = new Date(msg.timestamp * 1000).toLocaleTimeString();
      row.insertCell(1).textContent = "0x" + msg.id.toString(16).toUpperCase();
      row.insertCell(2).textContent = msg.data;
      count++;
      countEl.textContent = count;
      updateStatus(true);
    });
  </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/status')
def status():
    return jsonify({'connected': connected, 'message_count': message_count})

# Receive CAN messages from laptop and broadcast to UI
@socketio.on('can_message')
def handle_external_can_message(data):
    global message_count, connected
    connected = True
    message_count += 1
    socketio.emit('can_message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5050)
