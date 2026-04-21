import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

from qiskit.primitives import Sampler
from qiskit_machine_learning.algorithms import VQC
from qiskit.circuit.library import ZZFeatureMap

from qiskit.circuit.library import TwoLocal
from qiskit_algorithms.optimizers import COBYLA

app = FastAPI()

class Features(BaseModel):
    rate: float
    burst: float
    variance: float

# ---- TRAINING DATA (BEHAVIORAL) ----
X = np.array([
    [0.1, 0.1, 0.1],
    [0.2, 0.1, 0.2],
    [0.8, 0.7, 0.6],
    [0.9, 0.9, 0.9]
])
y = np.array([0, 0, 1, 1])

feature_map = ZZFeatureMap(3)
ansatz = TwoLocal(3, "ry", "cz", reps=2)

vqc = VQC(
    feature_map=feature_map,
    ansatz=ansatz,
    optimizer=COBYLA(maxiter=50),
    sampler=Sampler()
)

print("[QML] Training started")
vqc.fit(X, y)
print("[QML] Training completed")

@app.post("/predict")
def predict(f: Features):
    x = np.array([[f.rate, f.burst, f.variance]])
    pred = int(np.asarray(vqc.predict(x)).item())
    return {"prediction": "DOS_ATTACK" if pred == 1 else "NORMAL"}
