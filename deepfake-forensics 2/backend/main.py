"""
Deepfake Forensics Backend
Single-file FastAPI app: upload analysis + live-capture (extension) analysis.

Run:
    pip install fastapi uvicorn python-multipart opencv-python numpy --break-system-packages
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cv2
import numpy as np
import uuid
import os
import base64

app = FastAPI(title="Deepfake Forensics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)

# In-memory "database" -> swap for DynamoDB later, fine for a demo
RESULTS = {}


# ---------------------------------------------------------------------------
# Core scoring logic (shared by both upload + frame-capture flows)
# ---------------------------------------------------------------------------

def laplacian_score(gray_frame: np.ndarray) -> float:
    """Crude manipulation-artifact proxy: high-frequency detail variance.
    Stand-in for a real deepfake classifier (HF/PyTorch model) -- swap
    `score_frame()` below for a real model call when you have one wired up.
    """
    return cv2.Laplacian(gray_frame, cv2.CV_64F).var()


def score_frame(gray_frame: np.ndarray) -> float:
    return laplacian_score(gray_frame)


def normalize_to_confidence(raw_scores: list) -> list:
    """z-score normalize raw artifact scores into a 0-1 'confidence' scale."""
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
    """Placeholder for Amazon Transcribe + audio-artifact detection.
    Replace with a real call once you have AWS creds wired up:
      - transcribe.start_transcription_job(...) for timestamps/text
      - a separate audio-artifact model (pitch/timbre consistency) for anomalies
    """
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
    """Placeholder for C2PA Content Credentials check.
    Real version: use the `c2pa` python package to read embedded manifests:
        from c2pa import Reader
        reader = Reader.from_file(filepath)
        manifest = reader.get_active_manifest()
    """
    return {
        "c2pa_found": False,
        "note": "No Content Credentials (C2PA) manifest detected in file metadata.",
    }


def generate_report(video_segments: list, audio_segments: list, provenance: dict) -> str:
    """Placeholder for Amazon Bedrock / LLM reasoning step.
    Real version: feed this same structured JSON into a Bedrock/Claude prompt
    like: "Given these detector outputs, write a plain-English forensic summary."
    """
    lines = []
    for s in video_segments:
        lines.append(f"Face region shows manipulation artifacts from {s['start']}s to {s['end']}s.")
    for s in audio_segments:
        lines.append(f"Audio shows signs of alteration from {s['start']}s to {s['end']}s ({s['note']}).")
    if not provenance["c2pa_found"]:
        lines.append("No verifiable content provenance (C2PA) was found, which reduces confidence in authenticity.")
    if not lines:
        lines.append("No strong manipulation signals detected in this sample.")
    return " ".join(lines)


def build_response(file_id: str, timeline: list, video_segments: list,
                    audio_segments: list, provenance: dict) -> dict:
    report = generate_report(video_segments, audio_segments, provenance)
    result = {
        "file_id": file_id,
        "timeline": timeline,
        "video_segments": video_segments,
        "audio_segments": audio_segments,
        "provenance": provenance,
        "report": report,
    }
    RESULTS[file_id] = result
    return result


# ---------------------------------------------------------------------------
# Flow 1: full video upload (web app)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Flow 2: sampled frames from the browser extension (base64 JPEGs)
# ---------------------------------------------------------------------------

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
            header, b64data = f.split(",", 1)
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


# ---------------------------------------------------------------------------
# Retrieve a past result (for DynamoDB-style history, currently in-memory)
# ---------------------------------------------------------------------------

@app.get("/results/{file_id}")
async def get_result(file_id: str):
    return RESULTS.get(file_id, {"error": "not found"})


@app.get("/health")
async def health():
    return {"status": "ok"}
