from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

nodes = {}

incident = {
    "active": False,
    "attacked_node": None,
    "end_time": None
}

HOLD_TIME = 40  # seconds

class Update(BaseModel):
    node_id: str
    port: int
    status: str
    prediction: str

@app.post("/update")
def update(u: Update):
    now = time.time()

    # 🔥 Start global incident
    if u.status == "UNDER_ATTACK" and not incident["active"]:
        incident["active"] = True
        incident["attacked_node"] = u.node_id
        incident["end_time"] = now + HOLD_TIME

    # 🔓 End global incident
    if incident["active"] and now >= incident["end_time"]:
        incident["active"] = False
        incident["attacked_node"] = None
        incident["end_time"] = None
        nodes.clear()

    # 🔐 Apply global state
    if incident["active"]:
        if u.node_id == incident["attacked_node"]:
            nodes[u.node_id] = {
                "node_id": u.node_id,
                "port": u.port,
                "status": "UNDER_ATTACK",
                "prediction": "DOS_ATTACK"
            }
        else:
            nodes[u.node_id] = {
                "node_id": u.node_id,
                "port": u.port,
                "status": "PROTECTED",
                "prediction": "PEER_ALERT"
            }
    else:
        nodes[u.node_id] = {
            "node_id": u.node_id,
            "port": u.port,
            "status": "NORMAL",
            "prediction": "NORMAL"
        }

    return {"ok": True}

@app.get("/nodes")
def get_nodes():
    return nodes

@app.get("/incident")
def get_incident():
    return incident
