# Deepfake Forensics — prototype status

This sub-project is a separate browser/video concept, but the main repo has now pivoted to an audio-first prototype for the current hackathon scope.

## Current status

- The browser/video stack still exists in this folder as a separate prototype
- The root project is now focused on audio-based anomaly analysis and local explanation
- The goal is to prove the workflow before expanding back into multimodal video analysis

## What is already working here

- FastAPI service scaffolding for analysis requests
- Frontend upload flow and timeline/report output
- Extension-based frame capture for in-page video
- Mock scoring pipeline and local report generation

## What is still missing

- Real deepfake detector for faces or audio
- Real provenance verification
- Accurate spatial localization and face detection
- Human review/routing workflow
- Benchmarking against real-world manipulated samples

## Run locally

```bash
cd backend
pip install -r requirements.txt --break-system-packages
uvicorn main:app --reload --port 8000
```

```bash
cd frontend
npm install
npm run dev
```

## Recommendation

Treat this as an architectural prototype and a product-direction testbed. The root repo is the current “done now” path for audio-only analysis, while this folder remains the more ambitious multimodal expansion lane.
