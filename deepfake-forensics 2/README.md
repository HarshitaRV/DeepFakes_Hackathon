# Deepfake Forensics — current demo prototype

This folder is the active browser/video prototype for the hackathon pitch.

## What the current demo does

- Accepts a video upload
- Extracts sampled frames over time
- Scores each frame for visual artifact “weirdness” using a plain heuristic proxy
- Normalizes those scores to a 0–1 confidence curve
- Finds contiguous time ranges where the score spikes above a threshold
- Shows a red-highlighted confidence chart
- Lists the suspicious ranges in plain timestamps
- Produces a short plain-English summary such as:
  - “Face region shows manipulation artifacts from 4.2s to 9.8s. No content provenance found.”
- Displays provenance status as found / not found

## Current output contract

The app is built around this simple user-facing flow:

Input → Output

- Input: uploaded video or in-page captured frames
- Output:
  - chart of confidence over time
  - red highlighted suspicious zones
  - list of flagged start/end ranges
  - plain-English summary sentence
  - provenance result

This is the core product narrative and should stay intentionally simple for the demo.

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

## What still needs to be replaced later

- real deepfake model instead of heuristic artifact scoring
- real provenance verification instead of placeholder metadata checks
- more accurate face localization and temporal segmentation
- stronger audio detection pipeline
- robust benchmark set and model calibration

## Demo note

The current prototype is designed to contrast clearly:

- Real clip → quiet timeline, little/no risk signal
- Fake clip → spikes, red detection zones, suspicious ranges, evidence summary

That contrast is the whole pitch.
