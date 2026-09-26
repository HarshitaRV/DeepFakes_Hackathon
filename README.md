# DeepFakes_Hackathon

## Current state

This repo now contains two layers of work:

1. The active demo prototype in `deepfake-forensics 2/` is a browser/video workflow built around upload + frame sampling + confidence timeline + flagged segments + plain-English summary.
2. The root folder still includes supporting audio-analysis scripts and tests (`app.py`, `ml_pipeline.py`, `train_model.py`, etc.) that were used during the earlier audio-first exploration.

The main product story now is the simpler demo flow:

- Upload a video file or capture frames from a video already on a webpage
- Sample frames over time
- Score the frame-to-frame visual “weirdness” as a confidence curve
- Highlight suspicious time windows above a threshold
- Return a chart, flagged ranges, and one plain-English sentence explaining the evidence
- Show whether provenance/content credentials were found

This is intentionally a hackathon prototype, not a production-diagnostic system.

## What is working now

- Video upload + backend analysis flow in `deepfake-forensics 2/backend/main.py`
- Frame-based confidence timeline generation and segment extraction
- Red-highlighted suspicious zones in the UI
- Flagged time-range list with start/end timestamps
- Short plain-English summary sentence
- Provenance line indicating whether content credentials were found
- Frontend experience in `deepfake-forensics 2/frontend/src/App.tsx`
- Focused tests for the demo summary contract in `tests/test_demo_output.py`

## Demo behavior

For the pitch, the expected contrast is simple:

- Real clip: low, quiet confidence timeline; no meaningful flagged ranges
- Fake clip: confidence curve spikes; red zones appear; flagged ranges show the suspicious seconds; summary sentence names exactly where the manipulation happens

This is the core demo story: upload video → get back exactly which seconds looked fake, in plain English.

## Repo structure

- `app.py`: earlier audio prototype entry point
- `ml_pipeline.py`: audio feature extraction and training support
- `train_model.py`: lightweight audio model experimentation
- `evaluate_model.py`: evaluation utilities
- `deepfake-forensics 2/backend/main.py`: current upload + frame-analysis backend
- `deepfake-forensics 2/frontend`: current browser demo frontend
- `tests/`: validation and smoke tests
- `docs/`: product, scope, and planning materials
- `data/`: sample data and generated assets

## Run the current demo

Backend:

```bash
cd "DeepFakes_Hackathon/deepfake-forensics 2/backend"
pip install -r requirements.txt --break-system-packages
uvicorn main:app --reload --port 8000
```

Frontend:

```bash
cd "DeepFakes_Hackathon/deepfake-forensics 2/frontend"
npm install
npm run dev
```

Then open the local frontend URL shown by Vite and upload a short clip.

## Important note

The point of this project is to show a believable explainable demo, not to pretend the backend is a production-grade detector. The current prototype is intentionally limited to heuristic scoring, timestamped suspicious windows, and provenance reporting for a clear hackathon pitch.
