import subprocess
import sys
import time

PY = sys.executable

print("[STARTING] Backend")
subprocess.Popen([PY, "-m", "uvicorn", "backend.server:app", "--port", "8000"])

time.sleep(2)

print("[STARTING] QML")
subprocess.Popen([PY, "-m", "uvicorn", "qml.qml_predictor:app", "--port", "5000"])

time.sleep(3)

# 🔥 START 8 NODES HERE
BASE_PORT = 9001
for i in range(8):
    node_id = f"Node{i+1}"
    port = BASE_PORT + i
    subprocess.Popen([PY, "nodes/peer_node.py", node_id, str(port)])
    print(f"[STARTED] {node_id} on {port}")

print("\n✅ SYSTEM RUNNING")
print("Open frontend/index.html")
input("Press ENTER to stop")
