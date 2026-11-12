from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from rdkit import Chem, DataStructs
from rdkit.Chem import rdFingerprintGenerator
import joblib
import numpy as np

MODEL_PATH = Path(__file__).parent / "models" / "tox21_models.joblib"
ENDPOINTS = ["NR-AR", "NR-AR-LBD", "NR-AhR", "NR-aromatase", "NR-ER", "NR-ER-LBD", "NR-PPAR-gamma", "SR-ARE", "SR-ATAD5", "SR-HSE", "SR-MMP", "SR-p53"]
app = FastAPI(title="Tox21 SMILES Prediction API", version="1.0.0")
models = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None
generator = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=1024)

class PredictionRequest(BaseModel):
    smiles: str = Field(min_length=1, max_length=2000)

@app.get("/health")
def health():
    return {"status": "ok", "model_ready": models is not None}

@app.post("/predict")
def predict(payload: PredictionRequest):
    if models is None:
        raise HTTPException(status_code=503, detail="Tox21 model files are not installed on the prediction service.")
    mol = Chem.MolFromSmiles(payload.smiles)
    if mol is None:
        raise HTTPException(status_code=422, detail="The SMILES string could not be parsed. Please check its syntax.")
    canonical = Chem.MolToSmiles(mol)
    fp = generator.GetFingerprint(mol)
    arr = np.zeros((1024,), dtype=np.float32)
    DataStructs.ConvertToNumpyArray(fp, arr)
    output = []
    for endpoint in ENDPOINTS:
        model = models.get(endpoint)
        if model is None:
            continue
        probability = float(model.predict_proba(arr.reshape(1, -1))[0][1])
        output.append({"endpoint": endpoint, "label": "Predicted active" if probability >= 0.5 else "Predicted inactive", "probability_active": probability})
    return {"smiles": payload.smiles, "canonical_smiles": canonical, "predictions": output, "model_note": "Random Forest models trained on Tox21 assay labels using 1,024-bit radius-2 Morgan fingerprints. Probabilities are model estimates and are not clinical toxicity probabilities."}
