# Product Requirements Document (PRD)

## 1. Document Purpose
This document translates the use case in [README.md](../README.md) into a spec-driven development baseline for building an explainable multimodal deepfake forensics system.

The system is not a definitive real/fake detector. It is an evidence-based forensic assistant designed to identify suspicious manipulation patterns, localize them in time and space, and support human review.

---

## 2. Product Vision
Create a product that helps users understand whether media has been manipulated, where the manipulation happened, and how confident the system is—without hiding critical evidence behind a single binary label.

---

## 3. Problem Statement
Current deepfake detection tools often provide only a single confidence score, which is insufficient for journalists, reviewers, moderators, and everyday users. In practice, modern manipulations are often hybrid or partial edits: real footage combined with altered faces, cloned voices, or localized deepfake components.

The product must detect and explain these manipulations across video and audio, corroborate evidence with provenance signals, and route findings to human review rather than automatic action.

---

## 4. Goals
- Detect AI manipulation across video and audio modalities.
- Localize manipulation by frame range, timestamp range, and region where possible.
- Explain results in plain language.
- Corroborate findings with metadata and provenance signals.
- Support human review workflows for moderated action.
- Reduce false conclusions caused by black-box binary decisions.

## 5. Non-Goals
- Fully autonomous takedown decisions.
- Providing absolute legal certainty on authenticity.
- Guaranteeing detection of all future adversarial manipulations.
- Replacing human judgment in high-impact moderation decisions.

---

## 6. Target Users

### 6.1 Researchers / Journalists
Need: exact manipulated ranges, evidence trails, and clear explanations for reporting.

### 6.2 Content Reviewers / Creators
Need: simple verification before making claims or publishing content.

### 6.3 Everyday Users
Need: plain-language explanation rather than a raw detector score.

### 6.4 Trust & Safety / Moderation Teams
Need: triage signals and evidence summary before review or escalation.

---

## 7. User Needs and Outcomes

| User | Need | Desired Outcome |
| --- | --- | --- |
| Researcher | Understand manipulation extent | Timeline with exact frame/audio ranges |
| Journalist | Build evidence for reporting | Explainable report with provenance support |
| Creator | Validate authenticity before publishing | Resource-level explanation and risk tier |
| Everyday user | Understand suspicious media | Plain-language summary with uncertainty |
| Moderator | Triage suspicious content | Review queue recommendation and evidence summary |

---

## 8. Functional Requirements

### FR-01: Ingestion
The system shall accept uploaded media files and optionally URLs.

Acceptance criteria:
- A user can upload a video or audio file.
- A file is validated before processing.
- The system extracts visual and audio streams for analysis.

### FR-02: Multimodal Detection
The system shall analyze both video and audio streams for manipulation signals.

Required detection categories:
- Video: face-swap artifacts, blending boundaries, temporal inconsistencies, lip-sync mismatch
- Audio: cloning artifacts, splice points, unnatural prosody, spectral discontinuities

Acceptance criteria:
- The system returns per-modality suspicious segments.
- Each segment is associated with a confidence score.

### FR-03: Temporal and Spatial Localization
The system shall localize suspicious evidence in time and region.

Acceptance criteria:
- Video findings indicate affected frame or time ranges.
- Audio findings indicate affected timestamp windows.
- If available, face bounding boxes or region-level highlights are returned.

### FR-04: Provenance Checking
The system shall extract and assess provenance metadata when available.

Acceptance criteria:
- The system reads C2PA/content credentials if present.
- Metadata and EXIF details are surfaced.
- Re-encoding or compression artifacts are reported where feasible.

### FR-05: Explainability
The system shall generate plain-language explainers for non-technical users.

Acceptance criteria:
- Final output can be read without technical knowledge.
- Each conclusion references evidence and uncertainty.

### FR-06: Risk Triage
The system shall produce a risk tier and next-step recommendation.

Acceptance criteria:
- Output includes confidence and risk status.
- Recommendations differ for journalists, reviewers, and moderators.
- High-risk findings are routed to human review instead of auto-action.

### FR-07: Auditability
The system shall retain an evidence trail for review and accountability.

Acceptance criteria:
- Each report stores input metadata, detection outputs, and provenance scan results.
- The report supports chain-of-custody and internal review use cases.

### FR-08: Safety and Governance
The system shall protect sensitive outputs and avoid overconfident conclusions.

Acceptance criteria:
- No automated takedown is triggered from detection alone.
- High-detail forensic results have controlled access.

---

## 9. Non-Functional Requirements

### NFR-01: Accuracy on Real-World Media
The system must be evaluated against real-world compressed, re-uploaded, and partially manipulated media rather than only clean lab samples.

### NFR-02: Explainability
The system must present findings in a way that is understandable to non-technical users.

### NFR-03: Privacy and Consent
Handling of uploaded media must comply with consent and terms-of-service constraints.

### NFR-04: Performance
The system must support reasonable upload-to-insight latency for pilot use cases.

### NFR-05: Security
Sensitive outputs must be protected with access control and audit logging.

### NFR-06: Scalability
The architecture must allow future support for larger moderation queues and batch analysis.

---

## 10. Success Metrics
- Detection outputs align with human review decisions in pilot evaluation.
- Time-to-verify is reduced for suspicious media review.
- False positives and false negatives are tracked and reviewed.
- User comprehension of explanations is validated.
- Provenance findings improve confidence calibration.

---

## 11. Risks and Constraints

### Risk: Detector reliability gap
Mitigation: validate against real-world, not lab-only, datasets; express uncertainty clearly.

### Risk: Adversarial model drift
Mitigation: version model registry and retrain on schedule.

### Risk: Provenance coverage gaps
Mitigation: treat provenance as supporting evidence, not guaranteed proof.

### Risk: Misuse of forensic detail
Mitigation: access controls and limited detail views for public-facing flows.

---

## 12. Definition of Done
The product is ready for pilot release when:
- the core ingestion pipeline works
- video and audio detection produce segment-level evidence
- provenance checks run and are surfaced
- reports are understandable to target users
- human-review flow is operational
- legal/privacy review is documented
- benchmark results on real-world data are logged

---

## 13. Traceability Summary
This PRD maps directly to the README use case and ensures that all product decisions are traceable to the corresponding requirement.

Requirement chain:
User need → functional requirement → system capability → validation test → pilot metric
