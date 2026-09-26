import os
import tempfile

import librosa
import numpy as np
import streamlit as st


st.set_page_config(page_title="Audio Forensics Demo", page_icon="🎧")
st.title("Audio Forensics Demo")
st.caption("Audio-only local prototype for suspicious media detection and forensic reporting")


def extract_basic_audio_metadata(audio_path: str):
    try:
        y, sr = librosa.load(audio_path, sr=None)
    except Exception:
        return {
            "path": audio_path,
            "kind": "audio",
            "duration_seconds": 0,
            "sample_rate": 0,
            "channels": 0,
            "source": "local upload",
            "provenance": "No clear provenance chain detected",
        }

    duration = float(len(y)) / sr if sr else 0
    channels = 1 if len(y.shape) == 1 else y.shape[1]
    return {
        "path": audio_path,
        "kind": "audio",
        "duration_seconds": round(duration, 2),
        "sample_rate": int(sr),
        "channels": int(channels),
        "source": "local upload",
        "provenance": "No clear provenance chain detected",
    }


def detect_audio_anomalies(audio_path: str):
    try:
        y, sr = librosa.load(audio_path, sr=None)
    except Exception:
        return {"status": "Audio could not be analyzed", "suspicious_windows": []}

    signal = y if len(y.shape) == 1 else y[:, 0]
    energy = np.abs(signal)
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


def build_audio_report(metadata, audio_anomaly):
    lines = []
    lines.append("Summary: The uploaded audio was analyzed for suspicious signal anomalies.")
    lines.append(f"Duration: {metadata.get('duration_seconds', 0)} seconds")
    lines.append(f"Sample rate: {metadata.get('sample_rate', 0)} Hz")

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


uploaded = st.file_uploader("Upload a local audio file", type=["wav", "mp3", "m4a", "ogg"])

if uploaded is not None:
    temp_dir = tempfile.mkdtemp(prefix="audio_forensics_")
    save_path = os.path.join(temp_dir, uploaded.name)
    with open(save_path, "wb") as f:
        f.write(uploaded.getvalue())

    st.success(f"File saved locally: {uploaded.name}")

    st.subheader("Basic audio metadata")
    metadata = extract_basic_audio_metadata(save_path)
    st.json(metadata)

    st.subheader("Audio anomaly assessment")
    audio_anomaly = detect_audio_anomalies(save_path)
    st.json(audio_anomaly)

    st.subheader("Plain-language forensic summary")
    summary = build_audio_report(metadata, audio_anomaly)
    st.write(summary)

else:
    st.info("Upload a sample audio file to run the local analysis demo.")

    st.markdown("### Demo notes")
    st.markdown("- This prototype is intentionally audio-only for the current hackathon scope.")
    st.markdown("- It does not make a definitive real/fake claim.")
    st.markdown("- It highlights suspicious audio segments and recommends human review.")
