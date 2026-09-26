# Deepfake Forensics — Explainable Multimodal Manipulation Detector

Detects and localizes AI manipulation across video and audio, then corroborates
findings with media provenance (C2PA). Ships as both a web app and a browser
extension that analyzes video already playing on a page.

## Structure
```
backend/    FastAPI service — frame scoring, mock audio + provenance, report generation
frontend/   React + TypeScript + Recharts upload UI
extension/  Chrome MV3 extension — captures frames from in-page <video> elements
```

## 1. Run the backend
```bash
cd backend
pip install -r requirements.txt --break-system-packages
uvicorn main:app --reload --port 8000
```
Confirm it's up: `curl http://localhost:8000/health`

## 2. Run the frontend
```bash
cd frontend
npm install
npm run dev
```
Open the printed localhost URL, upload a video, get a timeline + report.

## 3. Load the extension
1. Go to `chrome://extensions`
2. Enable Developer mode (top right)
3. Click "Load unpacked" → select the `extension/` folder
4. Open any page with a `<video>` element, click the extension icon, hit
   "Analyze Video On Page"

Note: cross-origin videos without CORS headers will taint the canvas capture
(browser security, not a bug) — demo on your own test page or a self-hosted
video for a live demo.

## What's real vs. mocked right now
- **Real**: frame extraction, artifact-variance scoring, timeline generation,
  segment localization, full API + UI wiring, in-page video capture.
- **Mocked (clearly labeled in code)**: the actual deepfake classifier
  (`score_frame`), audio manipulation detection (`mock_audio_analysis`),
  C2PA provenance check (`check_provenance`), and the LLM-based report
  writer (`generate_report`). Each has a docstring noting exactly what real
  service (HF/PyTorch model, Amazon Transcribe, C2PA lib, Amazon Bedrock)
  it stands in for and how to wire it in.
