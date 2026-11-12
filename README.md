# AI Drug Toxicity Prediction Virtual Lab

Students enter only a molecular SMILES string. The application returns predicted activity for the 12 Tox21 assay endpoints. The dataset and model-training workflow are not exposed in the student interface.

## Architecture
- Frontend: Next.js on Vercel.
- Inference API: FastAPI + RDKit on Render (Docker).
- Models: endpoint-specific Random Forest classifiers trained from Tox21 using DeepChem ECFP fingerprints.
- Student input: SMILES only; Morgan fingerprints are generated automatically by RDKit.

## Deploy prediction API
1. In Render, create a new Blueprint and connect this repository.
2. Render reads `render.yaml`, builds the Docker image, downloads/loads Tox21 through DeepChem and trains 12 endpoint models.
3. Wait for the build to finish. Confirm `https://YOUR-API.onrender.com/health` reports `model_ready: true`.
4. Note the service URL.

## Deploy frontend on Vercel
1. Import this repository into Vercel.
2. Framework: Next.js; Root Directory: `./`; Build command: `npm run build`.
3. Add Environment Variable `TOXICITY_API_URL` = the Render service URL (for example `https://ai-drug-toxicity-api.onrender.com`).
4. Redeploy after adding the environment variable.

## Local frontend
```bash
npm install
npm run dev
```

## Train/test and scientific notes
The backend training script uses the public Tox21 benchmark internally; students do not upload or select datasets. DeepChem's Tox21 loader provides assay labels, where negative/missing values represent unmeasured entries and are excluded per endpoint during training. The script fits a final Random Forest for each endpoint using the available labelled benchmark compounds. This is a teaching screening model, not a validated clinical safety model. Its output probabilities are not calibrated clinical probabilities; predictions should be interpreted as endpoint-specific model estimates. For publication-grade use, run scaffold-split validation, report ROC-AUC/PR-AUC and calibration, tune thresholds, and externally validate.

## Model deployment note
The Docker build trains models during image construction and may take several minutes. The resulting model artifact is bundled into the API image; no student-facing dataset upload is provided.
