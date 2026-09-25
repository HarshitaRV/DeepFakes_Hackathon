# DeepFakes_Hackathon
Use Case: Explainable Multimodal Deepfake Forensics & Provenance Tool
Details & Purpose

## Quick Start

```bash
git clone https://github.com/HarshitaRV/DeepFakes_Hackathon.git
cd DeepFakes_Hackathon
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/run_hackathon_validation.py
streamlit run app.py --server.headless true --server.port 8501
```

Then open:

```text
http://localhost:8501
```

Deepfakes have evolved from wholesale fabrications to hybrid manipulations — a real body paired with an AI-generated face, or authentic footage with altered audio. Binary "real/fake" classification no longer serves platforms, journalists, or everyday users well, because it hides where and how content was altered. This use case defines an explainable, multimodal deepfake forensics agent that detects manipulation across video and audio, localizes it (which frames, which time window), and corroborates its findings against media provenance signals (C2PA metadata, upload history, re-encoding artifacts, etc.) — producing output like:

"Face manipulated in frames 140–190; audio altered from 0:18–0:24; no C2PA provenance chain found."

The purpose is to move from a black-box authenticity score to a transparent, evidence-backed forensic report that a non-technical person can act on.

## Local Setup and Run Guide

This project is designed to run locally as a lightweight hackathon prototype. The app entry point is `app.py`, the dependency list is in `requirements.txt`, and the validation workflow is in `scripts/run_hackathon_validation.py`.

### 1) Clone the repository

```bash
git clone https://github.com/HarshitaRV/DeepFakes_Hackathon.git
cd DeepFakes_Hackathon
```

### 2) Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3) Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The exact pinned package versions are in `requirements.txt` and were validated for the local demo environment.

### 4) Generate synthetic validation media (optional)

The repository already includes sample media under `test_data/`, but you can regenerate it at any time:

```bash
python scripts/generate_test_media.py
```

### 5) Run the automated validation checks

```bash
python scripts/run_hackathon_validation.py
```

This validation script checks that:
- the synthetic data is generated successfully
- the clean vs suspicious cases are evaluated correctly
- the overall prototype passes the local test workflow

### 6) Launch the app locally

```bash
streamlit run app.py --server.headless true --server.port 8501
```

Then open the app in a browser at:

```text
http://localhost:8501
```

### Quick start checklist

```bash
git clone https://github.com/HarshitaRV/DeepFakes_Hackathon.git
cd DeepFakes_Hackathon
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/run_hackathon_validation.py
streamlit run app.py --server.headless true --server.port 8501
```

### Expected outcome

- The validation script prints pass/fail checks for the clean and suspicious test cases.
- The Streamlit app starts successfully and loads on localhost:8501.
- The prototype is ready for local exploration, demoing, and iteration.

1. Business Problem
Deepfakes today are rarely 100% synthetic — they're composite manipulations (real footage + AI face swap + altered/cloned audio), which most legacy detectors aren't built to catch or explain.
Current detection tools output a single confidence score ("87% likely fake") with no explanation, which is not actionable for moderators, journalists, or end users and erodes trust when wrong.
Independent 2025–26 benchmarks show existing detectors degrade significantly on real-world, re-compressed social media content (vs. lab-clean datasets), creating a gap between published detector performance and production reality.
Platforms (Meta, Snap, Google, Bumble) are already treating this as a Trust & Safety priority, but mostly for impersonation/scam use cases, not for general-purpose, explainable, localized forensic analysis — leaving a gap for researchers, journalists, and content reviewers who need more than a moderation flag.
Mislabeling — either false positives (real content removed) or false negatives (fake content spreads) — carries reputational, legal, and misinformation risk.
2. Objective
Detect AI manipulation across both video and audio modalities in a single pipeline.
Localize manipulation spatially (which region of the frame — typically face) and temporally (which frames/timestamps).
Explain findings in plain language, not just a confidence score.
Corroborate with provenance signals (content credentials, metadata, edit history) to strengthen or weaken the forensic conclusion.
Support a "flag for review" workflow rather than automated takedown, preserving human judgment for high-stakes decisions.
3. Target Users
User Segment	Need
Researchers / journalists	Investigate suspicious media, identify exact manipulated segments, build evidence for reporting
Content creators / reviewers	Verify authenticity before making claims about products, people, or events
Everyday users	Upload a suspicious video, get a plain-language explanation instead of a raw detector score
Platform / moderation teams (future)	Triage suspicious content for human review rather than auto-deletion
4. What Should the Solution / Agent Do?
Ingest video/audio (upload or URL) and decompose into visual and audio streams.
Detect manipulation signals per modality:
Video: face-swap artifacts, blending boundaries, temporal flicker/inconsistency, lip-sync mismatch.
Audio: voice cloning artifacts, splice points, unnatural prosody, spectral discontinuities.
Localize findings: frame ranges for video, timestamp ranges for audio, and (where possible) spatial region (e.g., face bounding box).
Cross-check provenance: look for C2PA/Content Credentials, EXIF/metadata, re-encoding/compression history, and upload/platform history where available.
Generate a human-readable report: e.g., "Face manipulated in frames 140–190; audio altered from 0:18–0:24; no provenance chain found — recommend human review."
Assign a confidence + risk tier (not a binary verdict) and route to the appropriate downstream action (informational for end users; review queue for moderators).
Avoid auto-deletion — the agent flags and explains; humans decide, especially for ambiguous or high-profile cases.
5. Sample Questions / Use Cases
"Is this video of [public figure] endorsing a crypto investment real?"
"Which parts of this video were AI-generated — the face, the voice, or both?"
"Does this clip have a valid provenance/content-credential chain?"
"A user reported this video as a scam impersonation — what does the forensic report say before we act?"
"Show me exactly which frames and audio segments were altered, so I can cite it in my article."
6. Data / System Access Required
Uploaded or linked video/audio files (with appropriate consent/ToS handling).
Access to a deepfake detection model stack (video: face-manipulation/frame-consistency models; audio: voice-clone/splice detection models) — build or license.
Provenance/metadata infrastructure: C2PA verification, file metadata extraction, re-encoding/compression fingerprinting.
Optional: platform-side signals (upload history, account age/behavior) for platform-integrated deployments — requires moderation-team-level access, not available to public-facing versions.
Storage/logging for audit trail (especially important for journalist/legal use cases where chain-of-custody matters).
Compute for video/audio inference (frame extraction, spectrogram analysis) — likely GPU-backed.
7. ROI & Business Impact
Trust & Safety differentiation: positions the platform/product ahead of the binary-classifier approach competitors (Meta, Snap, Google) are still mostly using for impersonation-specific use cases — this is broader and more explainable.
Reduced moderation error cost: localized, evidence-backed flags reduce both wrongful takedowns (appeals, PR cost) and missed detections (misinformation/scam liability).
New user-facing product surface: an explainable "verify this video" tool could be offered directly to journalists, brands, or consumers — a monetizable trust product, not just a backend moderation tool.
Regulatory readiness: aligns with emerging deepfake/AI-content-labeling regulation (EU AI Act, proposed US state laws) ahead of enforcement deadlines.
Hard ROI is difficult to quantify pre-pilot; recommend a pilot with a defined moderation queue or journalist partner cohort to measure time-to-verify reduction and false-positive/negative rates before full-scale investment.
8. Priority & Risk

Priority: High — competitive urgency (Meta/Snap/Google actively investing), regulatory tailwinds, and a documented capability gap (real-world detector degradation) make this timely.

Risks:

Detector reliability gap: 2025–26 benchmarks show real-world performance drop vs. lab benchmarks — false positives/negatives carry real reputational and legal consequences.
Adversarial arms race: deepfake generation techniques evolve faster than detectors; the tool needs a retraining/update cadence, not a one-time build.
Explainability ≠ ground truth: a confident-sounding localized explanation can still be wrong; UX must communicate uncertainty, not just precision-sounding output.
Provenance gaps: most existing content lacks C2PA/Content Credentials today, limiting how much the corroboration step can actually add in the near term.
Misuse risk: the same forensic detail (frame/timestamp localization) could theoretically help bad actors refine future manipulations — needs access controls for sensitive output detail.
Human-in-the-loop dependency: the "flag, don't delete" model requires real moderation-team bandwidth; without it, the tool's output has nowhere to go.
9. Disclaimer

This document is a conceptual use-case framework, not a technical specification, vendor evaluation, or claim about any specific product's current accuracy. References to Meta, Snap, Google, and Bumble describe publicly reported directions in trust & safety and may not reflect their current internal capabilities in full. Any deployed system built from this framework would require rigorous, ongoing benchmarking against real-world (not lab-only) data, legal review (especially around biometric data, consent, and jurisdiction-specific AI/deepfake regulation), and should never be positioned as delivering definitive "real vs. fake" verdicts — only evidence-based signals for human judgment.