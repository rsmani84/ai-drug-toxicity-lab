"""Train one endpoint-specific Random Forest from the public Tox21 dataset.

Run from the backend directory after installing requirements:
    python train.py
DeepChem downloads the benchmark data into its local cache. The trained models
are saved to backend/models/tox21_models.joblib for the inference API.
"""
from pathlib import Path
import joblib
import numpy as np
import deepchem as dc
from sklearn.ensemble import RandomForestClassifier

ENDPOINTS = ["NR-AR", "NR-AR-LBD", "NR-AhR", "NR-aromatase", "NR-ER", "NR-ER-LBD", "NR-PPAR-gamma", "SR-ARE", "SR-ATAD5", "SR-HSE", "SR-MMP", "SR-p53"]
print("Downloading/loading Tox21 benchmark through DeepChem...")
train, valid, test, transformers = dc.molnet.load_tox21(featurizer="ECFP", splitter="scaffold", reload=False)
X = np.concatenate([ds.X for ds in (train, valid, test)], axis=0)
y = np.concatenate([ds.y for ds in (train, valid, test)], axis=0)
models = {}
for idx, endpoint in enumerate(ENDPOINTS):
    labels = y[:, idx]
    mask = np.isfinite(labels) & (labels >= 0)
    x_task, y_task = X[mask], labels[mask].astype(int)
    if len(np.unique(y_task)) < 2:
        print(f"Skipping {endpoint}: insufficient class diversity")
        continue
    clf = RandomForestClassifier(n_estimators=300, min_samples_leaf=2, class_weight="balanced_subsample", n_jobs=-1, random_state=42)
    clf.fit(x_task, y_task)
    models[endpoint] = clf
    print(f"{endpoint}: trained on {len(y_task)} measured labels")
out = Path(__file__).parent / "models"
out.mkdir(parents=True, exist_ok=True)
joblib.dump(models, out / "tox21_models.joblib", compress=3)
print(f"Saved {len(models)} endpoint models to {out / 'tox21_models.joblib'}")
