# DeepFakes_Hackathon

## Project status

This repo is currently focused on a lightweight audio-forensics prototype for a hackathon demo. The working direction is to analyze uploaded audio for suspicious discontinuities and present a plain-language forensic summary without pretending to make a definitive real/fake decision.

The project is intentionally scoped to a local, explainable prototype rather than a production deepfake detector.

## What is done

- Audio-only upload flow in app.py
- Basic metadata extraction for uploaded audio files
- Suspicious audio-window detection using signal magnitude heuristics
- Plain-language forensic report generation
- Synthetic clean/suspicious audio fixtures in test_data
- Validation script + focused tests for the audio-only flow
- Current repo cleanup to keep the project aligned with the simpler audio-first scope

## What still needs to be done

- Resolve dependency compatibility for this environment before full local validation passes cleanly
- Replace the heuristic audio detector with a real audio deepfake model or learned classifier
- Add provenance / metadata validation for content credentials, file history, and edit trails
- Expand the app to include a true review workflow and confidence/risk tiering
- Add stronger benchmark coverage on real-world media, not just synthetic test clips
- Optionally extend back to video/audio combined analysis once the audio foundation is solid

## Current local workflow

```bash
cd DeepFakes_Hackathon
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py --server.headless true --server.port 8501
```

Then open:

```text
http://localhost:8501
```

## Demo scope

This prototype is designed to answer a simpler question:

- Does this uploaded audio contain suspicious time windows that look inconsistent or manipulated?
- Can the system explain those segments in plain English and route them for human review?

It does not claim a final verdict on authenticity.

## Repo structure

- app.py: Streamlit audio-forensics prototype
- scripts/generate_test_media.py: generates synthetic clean/suspicious audio samples
- test_data: sample fixtures for local validation
- requirements.txt: Python dependencies
- docs: planning and product notes
- deepfake-forensics 2: separate prototype area for a fuller browser/video concept

## Recommended next milestone

1. Stabilize the local Python environment and dependency versions
2. Validate the audio pipeline on generated clean/suspicious samples
3. Replace the heuristic detector with a real model or model proxy
4. Add provenance + explainability pass
5. Decide whether to keep the project audio-only or reintroduce video analysis as a second phase

## Important note

This is a proof-of-concept for a hackathon, not a production trust system. The goal is to show the idea, the workflow, and the likely next engineering steps clearly.
