import socket
import threading
import time
import requests
import sys
import numpy as np
from collections import deque

# ---------------- CONFIG ----------------
NODE_ID = sys.argv[1]
PORT = int(sys.argv[2])

QML_URL = "http://127.0.0.1:5000/predict"
UPDATE_URL = "http://127.0.0.1:8000/update"
INCIDENT_URL = "http://127.0.0.1:8000/incident"

ATTACK_CONFIRM_TIME = 6

# ---------------- STATE ----------------
count = 0
history = deque(maxlen=10)
attack_start = None

lock = threading.Lock()

# ---------------- HELPERS ----------------
def incident_active():
    try:
        return requests.get(INCIDENT_URL, timeout=1).json()["active"]
    except:
        return False

# ---------------- LISTENER ----------------
def listener():
    global count
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", PORT))
    s.listen(300)
    print(f"[{NODE_ID}] Listening on {PORT}")

    while True:
        c, _ = s.accept()

        # 🚫 BLOCK TRAFFIC WHEN PROTECTED / ATTACK
        if incident_active():
            c.close()
            continue

        with lock:
            count += 1

        try:
            c.recv(1024)
            c.sendall(
                b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: text/plain\r\n"
                b"Content-Length: 2\r\n\r\nOK"
            )
        except:
            pass

        c.close()

# ---------------- ANALYZER ----------------
def analyzer():
    global count, attack_start

    while True:
        time.sleep(1)

        with lock:
            history.append(count)
            count = 0

        if len(history) < 5:
            continue

        h = list(history)

        rate = min(np.mean(h) / 20, 1.0)
        burst = max((h[-1] - np.mean(h[:-1])) / 20, 0)
        variance = min(np.var(h) / 50, 1.0)

        try:
            pred = requests.post(QML_URL, json={
                "rate": rate,
                "burst": burst,
                "variance": variance
            }, timeout=2).json()["prediction"]
        except:
            continue

        now = time.time()

        if pred == "DOS_ATTACK":
            if not attack_start:
                attack_start = now
            elif now - attack_start >= ATTACK_CONFIRM_TIME:
                requests.post(UPDATE_URL, json={
                    "node_id": NODE_ID,
                    "port": PORT,
                    "status": "UNDER_ATTACK",
                    "prediction": "DOS_ATTACK"
                })
        else:
            attack_start = None
            requests.post(UPDATE_URL, json={
                "node_id": NODE_ID,
                "port": PORT,
                "status": "NORMAL",
                "prediction": "NORMAL"
            })

# ---------------- START ----------------
threading.Thread(target=listener, daemon=True).start()
threading.Thread(target=analyzer, daemon=True).start()

while True:
    time.sleep(10)
