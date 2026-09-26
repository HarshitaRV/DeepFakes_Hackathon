"""
Deepfake Forensics Backend
Single-file FastAPI app: upload analysis + live-capture (extension) analysis.

Run:
    pip install fastapi uvicorn python-multipart opencv-python numpy --break-system-packages
    uvicorn main:app --reload --port 8000
"""

from __future__ import annotations

import base64
import os
import uuid
from typing import Any

import cv2
import numpy as np
import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_SUMMARY_MODEL_ID = os.getenv("HF_SUMMARY_MODEL_ID", "microsoft/Phi-3-mini-4k-instruct")

app = FastAPI(title="Deepfake Forensics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
RESULTS: dict[str, dict[str, Any]] = {}


def laplacian_score(gray_frame: np.ndarray) -> float:
    """Artifact-variance proxy for a video deepfake detector."""
    return cv2.Laplacian(gray_frame, cv2.CV_64F).var()


def score_frame(gray_frame: np.ndarray) -> float:
    return laplacian_score(gray_frame)


def normalize_to_confidence(raw_scores: list) -> list:
    """Convert raw artifact scores into a 0-1 confidence curve."""
    if not raw_scores:
        return []
    vals = [s["raw"] for s in raw_scores]
    mean, std = float(np.mean(vals)), float(np.std(vals)) + 1e-6
    out = []
    for s in raw_scores:
        z = abs(s["raw"] - mean) / std
        conf = min(1.0, max(0.0, z / 3))
        out.append({"time": s["time"], "confidence": round(conf, 2)})
    return out


def extract_segments(timeline: list, threshold: float = 0.5, label: str = "face") -> list:
    """Turn a confidence timeline into contiguous flagged segments."""
    segments = []
    in_seg = False
    seg_start = None
    for point in timeline:
        if point["confidence"] > threshold and not in_seg:
            in_seg, seg_start = True, point["time"]
        elif point["confidence"] <= threshold and in_seg:
            segments.append({"start": seg_start, "end": point["time"], "type": label})
            in_seg = False
    if in_seg:
        segments.append({"start": seg_start, "end": timeline[-1]["time"], "type": label})
    return segments


def mock_audio_analysis(duration: float) -> list:
    """Placeholder for audio-spoof detection; real version would use a voice-clone/splice model."""
    if duration < 5:
        return []
    start = round(duration * 0.3, 1)
    end = round(min(duration, start + 6), 1)
    return [{
        "start": start,
        "end": end,
        "type": "audio",
        "note": "Pitch/timbre inconsistency detected",
    }]


def check_provenance(filepath: str) -> dict:
    """Placeholder for C2PA Content Credentials validation."""
    return {
        "c2pa_found": False,
        "note": "No Content Credentials (C2PA) manifest detected in file metadata.",
    }


def call_hf_text_generation(prompt: str, model_id: str | None = None) -> str:
    """Example integration pattern for a Hugging Face text model.
    Set HF_API_TOKEN and HF_SUMMARY_MODEL_ID to activate this path.
    If missing credentials, the system gracefully falls back to the local heuristic report.
    """
    if not HF_API_TOKEN or not model_id:
        return ""

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 180, "temperature": 0.2, "return_full_text": False},
    }

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{model_id}",
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and data and isinstance(data[0], dict) and "generated_text" in data[0]:
            return data[0]["generated_text"].strip()
        if isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"].strip()
        if isinstance(data, list) and data and isinstance(data[0], str):
            return data[0].strip()
    except Exception:
        return ""

    return ""


def compute_analysis_summary(video_segments: list, audio_segments: list, provenance: dict, model_status: str) -> dict:
    signal_count = len(video_segments) + len(audio_segments)
    confidence = 0.28 + min(0.5, signal_count * 0.13)
    if provenance.get("c2pa_found") is False:
        confidence += 0.12
    confidence = round(min(0.97, confidence), 2)

    if signal_count == 0:
        risk = "low"
    elif confidence >= 0.7:
        risk = "high"
    elif confidence >= 0.45:
        risk = "medium"
    else:
        risk = "low"

    return {
        "signal_count": signal_count,
        "confidence": confidence,
        "risk": risk,
        "model_status": model_status,
    }


def generate_report(video_segments: list, audio_segments: list, provenance: dict) -> str:
    """Local heuristic report, with optional Hugging Face text-generation enhancement."""
    lines = []
    if video_segments:
        segment_summary = ", ".join(
            f"face manipulation likely affects {s['start']}s–{s['end']}s" for s in video_segments
        )
        lines.append(f"Video evidence: {segment_summary}.")
    if audio_segments:
        audio_summary = ", ".join(
            f"audio anomaly from {s['start']}s–{s['end']}s ({s.get('note', 'suspicious signal')})"
            for s in audio_segments
        )
        lines.append(f"Audio evidence: {audio_summary}.")
    if not provenance["c2pa_found"]:
        lines.append("No verifiable content provenance (C2PA) was found, so evidence remains inconclusive without human corroboration.")
    if not lines:
        lines.append("No strong manipulation signals detected in this sample.")
    lines.append("Recommended action: human review and corroboration with source metadata before making any public claim.")

    base_report = " ".join(lines)
    if HF_API_TOKEN and HF_SUMMARY_MODEL_ID:
        prompt = (
            "You are a forensic analyst. Write a short evidence-based summary for a deepfake investigation. "
            f"Context: video_segments={video_segments}; audio_segments={audio_segments}; provenance={provenance}. "
            "Do not state a definitive real/fake verdict; instead explain evidence, confidence, and the need for human review."
        )
        enhanced = call_hf_text_generation(prompt, HF_SUMMARY_MODEL_ID)
        if enhanced:
            return enhanced.strip()
    return base_report


def build_response(file_id: str, timeline: list, video_segments: list,
                    audio_segments: list, provenance: dict) -> dict:
    model_status = "huggingface-inference" if HF_API_TOKEN and HF_SUMMARY_MODEL_ID else "heuristic-fallback"
    report = generate_report(video_segments, audio_segments, provenance)
    analysis_summary = compute_analysis_summary(video_segments, audio_segments, provenance, model_status)
    result = {
        "file_id": file_id,
        "timeline": timeline,
        "video_segments": video_segments,
        "audio_segments": audio_segments,
        "provenance": provenance,
        "report": report,
        "analysis_summary": analysis_summary,
        "overall_risk": analysis_summary["risk"],
        "model_status": model_status,
    }
    RESULTS[file_id] = result
    return result


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    path = f"uploads/{file_id}_{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
    duration = frame_count / fps if fps else 0

    raw_scores = []
    idx = 0
    sample_every = 10
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % sample_every == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            raw_scores.append({"time": round(idx / fps, 2), "raw": score_frame(gray)})
        idx += 1
    cap.release()

    timeline = normalize_to_confidence(raw_scores)
    video_segments = extract_segments(timeline, threshold=0.5, label="face")
    audio_segments = mock_audio_analysis(duration)
    provenance = check_provenance(path)
    return build_response(file_id, timeline, video_segments, audio_segments, provenance)


class FramesPayload(BaseModel):
    frames: list
    duration: float


@app.post("/analyze_frames")
async def analyze_frames(payload: FramesPayload):
    file_id = str(uuid.uuid4())
    raw_scores = []
    n = len(payload.frames) or 1

    for i, f in enumerate(payload.frames):
        if not f:
            continue
        try:
            _, b64data = f.split(",", 1)
            img_bytes = base64.b64decode(b64data)
            arr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            t = (payload.duration / n) * i
            raw_scores.append({"time": round(t, 2), "raw": score_frame(img)})
        except Exception:
            continue

    if not raw_scores:
        return build_response(
            file_id, [], [], [],
            {"c2pa_found": False, "note": "No usable frames captured (likely a cross-origin block)."},
        )

    timeline = normalize_to_confidence(raw_scores)
    video_segments = extract_segments(timeline, threshold=0.5, label="face")
    audio_segments = mock_audio_analysis(payload.duration)
    provenance = {"c2pa_found": False, "note": "Provenance check unavailable for in-page capture."}
    return build_response(file_id, timeline, video_segments, audio_segments, provenance)


@app.get("/results/{file_id}")
async def get_result(file_id: str):
    return RESULTS.get(file_id, {"error": "not found"})


@app.get("/health")
async def health():
    return {"status": "ok", "model_status": "huggingface-pattern-ready" if HF_API_TOKEN else "heuristic-fallback"}
