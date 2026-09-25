# 1-Day Hackathon Task Board

## Goal
Build a simple local prototype that can upload a media file, analyze suspicious visual/audio signals, and present an evidence-based forensic summary without making a definitive real/fake claim.

## Team setup
Use a small team with clear ownership:
- Product/PM: scope, demo narrative, risk framing
- ML/AI engineer: forensic heuristics and model selection
- Backend engineer: upload pipeline, API, metadata handling
- Frontend engineer: UI and report page
- QA/demo lead: sample dataset, validation, presentation

---

## Task board

| Time | Task | Owner | Deliverable | Done when |
| --- | --- | --- | --- | --- |
| 9:00–9:30 | Kickoff, scope lock, spec review | All | Final MVP scope | Team agrees on what is in / out of scope |
| 9:30–10:00 | Environment setup | Backend + AI | Python env and package install | Local environment works |
| 10:00–11:00 | Project skeleton | Backend + Frontend | App structure and upload UI | File upload works locally |
| 11:00–12:30 | Video extraction + metadata | AI + Backend | Frame extraction and file metadata | Input media can be processed |
| 12:30–13:30 | Lunch / buffer | — | — | — |
| 13:30–15:00 | Video anomaly heuristics | AI engineer | Suspicious frame ranges | Time-based video findings generated |
| 15:00–16:00 | Audio anomaly heuristics | AI engineer | Suspicious time windows | Audio findings generated |
| 16:00–16:45 | Provenance summary | Backend | Metadata + provenance report | Missing/available provenance displayed |
| 16:45–17:30 | Report generation + UX | Frontend | Plain-language summary page | Demo narrative is readable |
| 17:30–18:00 | Test sample validation | QA/demo | 2–3 sample runs | App works on sample data |
| 18:00–18:30 | Final demo prep | All | Demo script | Team ready to present |

---

## MVP scope checklist
- Upload local media file
- Extract video frames and audio signal
- Detect suspicious segments in video
- Detect suspicious segments in audio
- Show metadata/provenance summary
- Show plain-language report
- Recommend human review instead of auto-decision
- Run locally on a laptop

---

## Out-of-scope for the hackathon
- Production-grade real-time cloud inference
- Auto takedown logic
- Full legal/compliance review pipeline
- Large-scale model training
- Multi-user deployment infrastructure
- High-volume moderation queue

---

## Definition of done for the hackathon
The prototype is successful when:
- the app runs locally
- a user can upload a sample clip
- suspicious segments are highlighted
- a plain-language evidence report is shown
- the system clearly communicates uncertainty
- the demo fits in a short presentation time
