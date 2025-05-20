# can_bridge_client.py

import can
import socketio
import time

# Set up Socket.IO client
sio = socketio.Client()

@sio.event
def connect():
    print("✅ Connected to ERGON server")

@sio.event
def disconnect():
    print("❌ Disconnected from ERGON server")

# Replace with your deployed Render server URL
sio.connect('https://your-ergon-app.onrender.com')

# Setup CAN interface
can_interface = 'pcan'
can_channel = 'PCAN_USBBUS1'  # Adjust as per your hardware
bus = can.interface.Bus(channel=can_channel, bustype=can_interface)

print("🎯 Starting CAN bridge...")

while True:
    try:
        msg = bus.recv(timeout=1)
        if msg:
            hex_data = ' '.join(f'{byte:02X}' for byte in msg.data)
            sio.emit('can_message', {
                'timestamp': msg.timestamp,
                'id': msg.arbitration_id,
                'data': hex_data
            })
    except Exception as e:
        print("⚠️ Error reading/sending CAN message:", e)
        time.sleep(1)
