# AI Drug Toxicity Prediction Virtual Lab

A single Next.js application intended for deployment on Vercel. Students enter only a SMILES string; RDKit.js runs in the browser to validate/canonicalize the structure and calculate basic molecular descriptors.

## Six intended toxicity endpoints
- Acute oral toxicity
- Acute dermal toxicity
- Acute inhalation toxicity
- Skin irritation and corrosion
- Eye irritation and corrosion
- Skin sensitization

## Current functionality and limitation
The current frontend performs SMILES parsing and descriptor calculation with RDKit.js. The six endpoint model slots are intentionally marked as not yet configured. No toxicity probabilities are generated until suitable endpoint-specific training datasets and validated model weights are added. Tox21 endocrine-disruption models are not substitutes for these endpoints.

## Deploy on Vercel only
1. Import this repository into Vercel.
2. Framework preset: Next.js.
3. Root Directory: `./`.
4. Build command: `npm run build`.
5. No separate Render service or `TOXICITY_API_URL` environment variable is required for the current SMILES analysis interface.

## Scientific requirements before prediction release
Each endpoint needs curated, consistently labelled data, a documented unit/class definition (especially for acute toxicity), scaffold-aware validation, class-imbalance handling, independent test evaluation, and calibration/threshold review. Do not label the output as clinical or regulatory safety. A model result is a computational hazard-screening estimate, not experimental proof.
