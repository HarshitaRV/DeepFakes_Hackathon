import os
from pathlib import Path

import cv2
import librosa
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = ROOT / "test_data"


def detect_video_anomaly(path: str):
    cap = cv2.VideoCapture(path)
    prev = None
    diffs = []

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev is not None:
            diffs.append(float(np.mean(np.abs(gray.astype(np.float32) - prev.astype(np.float32)))))
        prev = gray

    cap.release()
    if not diffs:
        return 0

    mean = float(np.mean(diffs))
    std = float(np.std(diffs))
    threshold = mean + 1.5 * std
    suspicious = sum(1 for v in diffs if v > threshold)
    return suspicious


def detect_audio_anomaly(path: str):
    y, sr = librosa.load(path, sr=None)
    energy = np.abs(y)
    frame_size = max(1, len(energy) // 200)
    chunks = [energy[i:i + frame_size] for i in range(0, len(energy), frame_size)]
    mags = [float(np.mean(np.abs(chunk))) for chunk in chunks if len(chunk) > 0]

    if not mags:
        return 0

    mean = float(np.mean(mags))
    std = float(np.std(mags))
    threshold = mean + 1.5 * std
    suspicious = sum(1 for v in mags if v > threshold)
    return suspicious


def run_case(case_name: str, video_name: str, audio_name: str, expected: str):
    video_path = TEST_DIR / video_name
    audio_path = TEST_DIR / audio_name

    video_score = detect_video_anomaly(str(video_path))
    audio_score = detect_audio_anomaly(str(audio_path))

    if expected == "clean":
        video_ok = video_score < 10
        audio_ok = audio_score == 0
    elif expected == "suspicious":
        video_ok = video_score >= 10
        audio_ok = audio_score > 0
    else:
        raise ValueError(f"Unknown expected state: {expected}")

    overall = video_ok and audio_ok
    return {
        "name": case_name,
        "expected": expected,
        "video_name": video_name,
        "audio_name": audio_name,
        "video_score": video_score,
        "audio_score": audio_score,
        "video_ok": video_ok,
        "audio_ok": audio_ok,
        "overall_pass": overall,
    }


def main():
    cases = [
        ("clean-case", "clean_clip.mp4", "clean_audio.wav", "clean"),
        ("suspicious-case", "suspicious_clip.mp4", "suspicious_audio.wav", "suspicious"),
    ]

    print("Running evaluation cases...\n")
    results = [run_case(case_name, video_name, audio_name, expected) for case_name, video_name, audio_name, expected in cases]

    total = len(results)
    passed = sum(1 for r in results if r["overall_pass"])

    for result in results:
        status = "PASS" if result["overall_pass"] else "FAIL"
        print(f"[{status}] {result['name']} | expected={result['expected']} | video={result['video_name']} score={result['video_score']} | audio={result['audio_name']} score={result['audio_score']}")

    print(f"\nSummary: {passed}/{total} cases passed")
    if passed != total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
