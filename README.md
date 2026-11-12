# AI Virtual Lab: Drug Toxicity Prediction

Standalone Next.js teaching application for GitHub and Vercel.

## Current features
- Explore the 12 Tox21 assay endpoints.
- Upload faculty-prepared CSV data with SMILES, assay labels (1, 0, blank), and numeric descriptor columns.
- Preserve blank labels as untested/missing, not inactive.
- Fit an educational Gaussian Naive Bayes baseline using supplied descriptors.
- Descriptor-based prediction sandbox and a short student knowledge check.

## Public dataset
Official NIH/NCATS Tox21 challenge data: https://tripod.nih.gov/tox21/challenge/data.jsp

The app does not automatically download or preprocess the public dataset. Prepare a CSV with a `smiles` column, one or more endpoint columns, and numeric descriptors such as MW, LogP, TPSA, HBD, HBA, RotB, AromaticRings and HeavyAtoms.

## Run locally
```bash
npm install
npm run dev
```

## Vercel
Import this repository. Select Next.js, keep Root Directory as `./`, and use `npm run build`.

## Scientific limitations
This is an educational baseline, not a validated drug-safety model. Tox21 labels are specific to individual in-vitro assays and do not establish clinical safety or toxicity. This version does not calculate descriptors from SMILES, render 2D/3D structures, automatically import Tox21, perform independent test-set validation, or persist student records to a shared database. Assessment data is limited to the current browser session. Do not use outputs for medical or regulatory decisions.
