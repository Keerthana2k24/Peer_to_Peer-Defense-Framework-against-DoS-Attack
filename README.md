## A Decentralized Peer to Peer Defense Framework Against DoS Attacks using Quantum Machine Learning
This project implements a decentralized peer-to-peer (P2P) defense system to detect and mitigate Denial-of-Service (DoS) attacks using Quantum Machine Learning (QML).
Each peer node independently monitors its incoming traffic, collaborates with other nodes during attacks, and enforces coordinated protection and automatic recovery.
The system simulates real-world attack scenarios and visualizes node behavior through a real-time interactive dashboard.

## Objectives
- Detect DoS attacks based on traffic behavior, not static thresholds

- Enable peer-to-peer coordination without a central controller

- Use Quantum ML (Qiskit VQC) for intelligent attack prediction

- Enforce temporary protection and automatic recovery

- Provide a live dashboard for monitoring node states

## System Architecture 

**1. Peer Nodes**

- Act as independent servers

- Monitor incoming TCP traffic

- Extract traffic features

**2. Feature Extraction**

- Request rate

- Burst behavior

- Traffic variance

**3. Quantum ML Engine**

- Variational Quantum Classifier (VQC) implemented using Qiskit

- Classifies traffic as NORMAL or DOS_ATTACK

**4. Backend Coordination Service**

- Collects node status updates

- Triggers peer protection

- Manages global recovery timing

**5. Frontend Dashboard**

- Visualizes all node states

- Shows NORMAL / UNDER_ATTACK / PROTECTED

- Updates in real time

**6. Attack Simulation**

- Apache Benchmark (ab)

- Generates realistic DoS traffic

## Project Structure
 ```
P2P_QML_DoS_Demo/
│
├── backend/
│   └── server.py
│
├── qml/
│   └── qml_predictor.py
│
├── nodes/
│   └── peer_node.py
│
├── frontend/
│   └── index.html
│
├── attack/
│   └── dos_attack.py
│
├── run_all.py
├── requirements.txt
└── README.md
```
## Technologies Used
- **Programming Language:**	Python
- **Networking:**	TCP Sockets, Multithreading
- **Quantum ML:**	Qiskit, VQC
- **Backend:** FastAPI
- **Frontend:**	HTML, CSS, JavaScript
- **Attack Simulation:**	Apache Benchmark (ab)
- **Visualization:**	RESTAPI
  
## Installation & Setup
- 1️⃣ Download code directory from the below drive link:
  https://1drv.ms/f/c/50a59d4a5bd9ec58/IgBQJ0TkVJP3Q5JachJlr-MiAV7oj-xs-4snyMR6SVKQVMg?e=plpsjr
```
cd P2P_QML_DoS_Demo -copy
```
- 2️⃣ Create Virtual Environment
```
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```
-▶️ Running the System - Start All Components (One Command)
```
python run_all.py
```
This will automatically start:
- QML service
- Backend coordination server
- Multiple peer nodes
- Frontend dashboard
In another terminal,
```
frontend/index.html
```

- **Simulating a DoS Attack**
Using Apache Benchmark (Linux / Windows)
```
ab -n 50000 -c 300 http://127.0.0.1:9001/
```
- -n → Total number of requests
- -c → Concurrent requests
- 9001 → Target node port (simulate on any node using its port number)
