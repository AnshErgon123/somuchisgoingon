import socketio
import can
import time

# ✅ UPDATE with your actual deployed server URL
SERVER_URL = "https://somuchisgoingon-6.onrender.com"  # e.g. "https://ergon-server.onrender.com"

# Socket.IO client setup
sio = socketio.Client()

@sio.event
def connect():
    print("✅ Connected to ERGON server")

@sio.event
def disconnect():
    print("❌ Disconnected from ERGON server")

@sio.event
def connect_error(data):
    print("❌ Connection failed:", data)

# Try connecting to the server
try:
    sio.connect(SERVER_URL)
except Exception as e:
    print(f"❌ Connection error: {e}")
    exit()

# Setup CAN interface — update channel if needed
can_interface = "pcan"  # Use 'pcan' for Peak-CAN device
can_channel = "PCAN_USBBUS1"

try:
    bus = can.interface.Bus(channel=can_channel, interface=can_interface)
except Exception as e:
    print(f"❌ CAN interface error: {e}")
    sio.disconnect()
    exit()

print("🎯 Listening for CAN messages...")

try:
    while True:
        message = bus.recv(timeout=1)
        if message:
            data = {
                "timestamp": time.time(),
                "id": message.arbitration_id,
                "data": list(message.data),
                "dlc": message.dlc
            }
            sio.emit("can_data", data)
            print("📤 Sent:", data)
except KeyboardInterrupt:
    print("🛑 Exiting...")
finally:
    bus.shutdown()
    sio.disconnect()
