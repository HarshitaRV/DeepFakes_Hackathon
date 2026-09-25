import os
import json
import tempfile
from pathlib import Path

import cv2
import librosa
import numpy as np
import streamlit as st


st.set_page_config(page_title="Deepfake Forensics Demo", page_icon="🧪")
st.title("Explainable Media Forensics Demo")
st.caption("Local hackathon prototype for suspicious media detection and forensic reporting")


def extract_basic_video_metadata(video_path: str):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps if fps else 0
    cap.release()
    return {
        "path": video_path,
        "frames": frame_count,
        "fps": fps,
        "width": width,
        "height": height,
        "duration_seconds": round(duration, 2),
        "source": "local upload",
        "provenance": "No clear provenance chain detected",
    }


def detect_video_anomalies(video_path: str):
    cap = cv2.VideoCapture(video_path)
    previous = None
    diffs = []

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if previous is not None:
            diff = np.mean(np.abs(gray.astype(np.float32) - previous.astype(np.float32)))
            diffs.append(diff)
        previous = gray

    cap.release()

    if not diffs:
        return {"status": "No strong temporal anomalies detected", "suspicious_frames": []}

    mean_diff = float(np.mean(diffs))
    std_diff = float(np.std(diffs))
    threshold = mean_diff + (1.5 * std_diff)
    suspicious = [i for i, v in enumerate(diffs, start=1) if v > threshold]

    if not suspicious:
        return {"status": "No strong temporal anomalies detected", "suspicious_frames": []}

    suspicious_ranges = []
    start = suspicious[0]
    prev = suspicious[0]
    for current in suspicious[1:]:
        if current - prev > 1:
            suspicious_ranges.append((start, prev))
            start = current
        prev = current
    suspicious_ranges.append((start, prev))

    return {
        "status": "Suspicious visual inconsistencies detected",
        "suspicious_frames": suspicious_ranges,
        "mean_diff": round(mean_diff, 4),
        "threshold": round(threshold, 4),
    }


def detect_audio_anomalies(audio_path: str):
    try:
        y, sr = librosa.load(audio_path, sr=None)
    except Exception:
        return {"status": "Audio could not be analyzed", "suspicious_windows": []}

    energy = np.abs(y)
    frame_size = max(1, len(energy) // 200)
    chunks = [energy[i:i + frame_size] for i in range(0, len(energy), frame_size)]
    chunk_magnitudes = [float(np.mean(np.abs(chunk))) for chunk in chunks if len(chunk) > 0]

    if not chunk_magnitudes:
        return {"status": "Audio could not be analyzed", "suspicious_windows": []}

    mean_mag = float(np.mean(chunk_magnitudes))
    std_mag = float(np.std(chunk_magnitudes))
    threshold = mean_mag + (1.5 * std_mag)

    suspicious_indices = [i for i, v in enumerate(chunk_magnitudes) if v > threshold]
    if not suspicious_indices:
        return {"status": "No strong audio discontinuities detected", "suspicious_windows": []}

    ranges = []
    start = suspicious_indices[0]
    prev = suspicious_indices[0]
    for idx in suspicious_indices[1:]:
        if idx - prev > 1:
            ranges.append((start, prev))
            start = idx
        prev = idx
    ranges.append((start, prev))

    suspicious_windows = []
    for start_idx, end_idx in ranges:
        start_time = round((start_idx * frame_size) / sr, 2)
        end_time = round((end_idx * frame_size) / sr, 2)
        suspicious_windows.append({"start": start_time, "end": end_time})

    return {
        "status": "Suspicious audio discontinuities detected",
        "suspicious_windows": suspicious_windows,
        "threshold": round(threshold, 4),
    }


def build_report(metadata, video_anomaly, audio_anomaly):
    lines = []
    lines.append("Summary: The uploaded media was analyzed for suspicious visual and audio signals.")
    lines.append(f"Duration: {metadata.get('duration_seconds', 0)} seconds")
    lines.append(f"Resolution: {metadata.get('width', 0)}x{metadata.get('height', 0)}")

    if video_anomaly["suspicious_frames"]:
        frames = video_anomaly["suspicious_frames"]
        first = frames[0]
        last = frames[-1]
        lines.append(f"Video suspicion: frames {first[0]}-{last[1]} were flagged as potentially inconsistent.")
    else:
        lines.append("Video suspicion: no strong temporal anomaly detected.")

    if audio_anomaly["suspicious_windows"]:
        windows = audio_anomaly["suspicious_windows"]
        sample = windows[0]
        lines.append(f"Audio suspicion: suspicious segment found between {sample['start']}s and {sample['end']}s.")
    else:
        lines.append("Audio suspicion: no strong audio discontinuity detected.")

    lines.append("Provenance: " + metadata.get("provenance", "No provenance data available."))
    lines.append("Risk tier: Medium")
    lines.append("Recommended action: Human review.")
    return "\n".join(lines)


uploaded = st.file_uploader("Upload a local video", type=["mp4", "mov", "avi", "mkv", "wav", "mp3"])

if uploaded is not None:
    temp_dir = tempfile.mkdtemp(prefix="deepfake_demo_")
    save_path = os.path.join(temp_dir, uploaded.name)
    with open(save_path, "wb") as f:
        f.write(uploaded.getvalue())

    st.success(f"File saved locally: {uploaded.name}")

    st.subheader("Basic media metadata")
    metadata = extract_basic_video_metadata(save_path)
    st.json(metadata)

    st.subheader("Video anomaly assessment")
    video_anomaly = detect_video_anomalies(save_path)
    st.json(video_anomaly)

    st.subheader("Audio anomaly assessment")
    audio_anomaly = detect_audio_anomalies(save_path)
    st.json(audio_anomaly)

    st.subheader("Plain-language forensic summary")
    summary = build_report(metadata, video_anomaly, audio_anomaly)
    st.write(summary)

else:
    st.info("Upload a sample media file to run the local analysis demo.")

    st.markdown("### Demo notes")
    st.markdown("- This is a lightweight local prototype for a hackathon.")
    st.markdown("- It does not make a definitive real/fake claim.")
    st.markdown("- It highlights suspicious video/audio segments and recommends human review.")
