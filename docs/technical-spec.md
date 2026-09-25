# Technical Specification

## 1. Objective
Define the technical architecture and implementation requirements for an explainable multimodal deepfake forensic agent.

This system is designed to identify manipulated regions in media, explain the findings, and support human review. It does not produce a definitive real/fake verdict.

---

## 2. Architecture Overview

The system comprises the following subsystems:

1. Ingestion and validation
2. Preprocessing and feature extraction
3. Video forensics analysis
4. Audio forensics analysis
5. Provenance and metadata analysis
6. Evidence fusion and risk scoring
7. Human-readable report generation
8. Audit logging and review workflow

---

## 3. System Components

### 3.1 Ingestion Service
Responsibilities:
- accept file upload or URL input
- validate accepted formats
- store raw media securely
- create immutable input record for audit

Inputs:
- file object or source URL
- optional user metadata and case ID

Outputs:
- media ID
- file metadata
- extracted media artifact references

### 3.2 Preprocessing Pipeline
Responsibilities:
- unpack video into frames
- normalize image size and quality
- extract audio waveform
- generate spectrograms and signal features
- detect media quality degradation signs

Outputs:
- frame sequence
- audio signal representation
- quality metadata
- timing map

### 3.3 Video Forensics Engine
Responsibilities:
- detect face manipulation and inconsistencies
- locate suspicious timeline segments
- estimate manipulated regions with bounding boxes if possible

Model categories:
- face swap / synthetic face detection
- blending boundary detection
- motion inconsistency analysis
- temporal flicker analysis
- lip-sync mismatch checks

Outputs:
- list of suspicious segments
- confidence values
- region coordinates
- frame-level evidence

### 3.4 Audio Forensics Engine
Responsibilities:
- detect voice cloning and audio splicing
- identify suspicious time windows
- analyze prosody and spectral continuity

Model categories:
- voice clone detection
- splice artifact detection
- spectral discontinuity detection
- prosody irregularity checks

Outputs:
- suspicious audio segments
- confidence values
- timestamps
- signal evidence summary

### 3.5 Provenance Engine
Responsibilities:
- inspect media metadata
- verify C2PA / content credentials
- extract EXIF and file history signals
- assess re-encoding and compression artifacts

Outputs:
- provenance status
- metadata summary
- confidence contribution for final assessment

### 3.6 Fusion and Risk Scoring
Responsibilities:
- combine evidence from video, audio, and provenance
- assign confidence and risk tier
- generate decision support output for human review

Rules:
- no binary verdict required
- uncertainty must be preserved in scoring
- outputs should indicate supporting vs contradicting evidence

### 3.7 Reporting Engine
Responsibilities:
- generate human-readable summaries
- prepare reviewer-friendly evidence cards
- format timeline and findings for UI or API clients

Example output:
- “Face manipulation likely present in frames 140–190.”
- “Audio manipulation likely present from 0:18–0:24.”
- “No provenance chain found; recommend human review.”

### 3.8 Audit and Review Service
Responsibilities:
- maintain immutable logs
- record model versions
- retain case history
- support moderation workflow routing

---

## 4. Data Contracts

### 4.1 Media Upload Schema
```json
{
  "media_id": "string",
  "source_type": "upload|url",
  "file_name": "string",
  "mime_type": "video/mp4",
  "uploaded_at": "ISO-8601",
  "user_context": "string|null"
}
```

### 4.2 Detection Segment Schema
```json
{
  "modality": "video|audio",
  "start_time": 12.5,
  "end_time": 18.2,
  "confidence": 0.87,
  "evidence_type": "face_swap|voice_clone|splicing|spectral_anomaly",
  "bbox": { "x": 120, "y": 80, "w": 200, "h": 220 },
  "notes": "string"
}
```

### 4.3 Provenance Result Schema
```json
{
  "has_c2pa": true,
  "credential_status": "valid|missing|invalid",
  "metadata_summary": "string",
  "compression_signals": ["re-encoded", "social_platform_export"],
  "risk_adjustment": 0.15
}
```

### 4.4 Final Report Schema
```json
{
  "case_id": "string",
  "overall_risk_tier": "low|medium|high",
  "confidence": 0.78,
  "summary": "string",
  "video_findings": [],
  "audio_findings": [],
  "provenance_findings": [],
  "recommended_action": "informational|human_review|escalate"
}
```

---

## 5. Functional Workflow

1. User uploads media.
2. Validation and metadata extraction occur.
3. Frame and audio streams are extracted.
4. Video and audio forensic models run independently.
5. Provenance checks are performed.
6. Evidence is merged to assign risk and confidence.
7. A human-readable report is produced.
8. Report is stored and routed for review if needed.

---

## 6. Edge Cases and Failure Handling

### Missing provenance metadata
- Report as missing, not as proof of forgery.

### Low-quality or heavily compressed media
- Lower confidence and mark results as uncertain.

### Ambiguous manipulation
- Return medium risk and recommend human review.

### Unsupported file types
- Reject early with clear validation message.

---

## 7. Security and Compliance Requirements
- Restrict high-detail forensic output to authorized reviewers.
- Apply consent and privacy checks before media processing.
- Record audit logs for model version, media hash, and report generation.
- Ensure legal review around biometric and identity-sensitive use cases.

---

## 8. Validation Strategy

The system must be validated on:
- clean synthetic deepfakes
- partial manipulations
- social-media compressed clips
- audio-only and video-only edits
- real-world edge cases with limited metadata

Metrics:
- precision/recall for segment localization
- uncertainty calibration
- false positive/negative rates in review workflow
- report usability by non-technical users

---

## 9. Implementation Roadmap Alignment

### Phase 1
- media ingestion and validation
- preprocessing
- baseline detection pipeline

### Phase 2
- provenance checks
- risk scoring and evidence fusion
- reporting layer

### Phase 3
- review workflow and logs
- pilot benchmarking
- iteration based on real usage data

---

## 10. Non-Technical Design Principle
This architecture should always prioritize evidence and transparency over binary judgments. The system exists to support investigation, not automate irreversible conclusions.
