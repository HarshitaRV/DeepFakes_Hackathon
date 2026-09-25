import os
from pathlib import Path

import cv2
import numpy as np
from scipy.io import wavfile


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "test_data"
DATA_DIR.mkdir(exist_ok=True)


def generate_clean_video(path: Path, seconds: float = 4.0, fps: int = 24, width: int = 640, height: int = 360):
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(path), fourcc, fps, (width, height))
    total_frames = int(seconds * fps)

    for i in range(total_frames):
        t = i / fps
        img = np.zeros((height, width, 3), dtype=np.uint8)
        img[:] = (30, 40, 60)

        cx = int(width / 2 + 30 * np.sin(2 * np.pi * t / 2.8))
        cy = int(height / 2 + 12 * np.sin(2 * np.pi * t / 1.9))

        cv2.circle(img, (cx, cy), 52, (200, 200, 210), -1)
        cv2.circle(img, (cx - 16, cy - 8), 8, (40, 40, 40), -1)
        cv2.circle(img, (cx + 16, cy - 8), 8, (40, 40, 40), -1)
        cv2.ellipse(img, (cx, cy + 16), (18, 8), 0, 0, 180, (70, 70, 70), -1)
        writer.write(img)

    writer.release()


def generate_suspicious_video(path: Path, seconds: float = 4.0, fps: int = 24, width: int = 640, height: int = 360):
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(path), fourcc, fps, (width, height))
    total_frames = int(seconds * fps)

    for i in range(total_frames):
        t = i / fps
        img = np.zeros((height, width, 3), dtype=np.uint8)
        img[:] = (15, 20, 25)

        if 1.0 <= t <= 2.8:
            flicker = 1.4 + 0.8 * np.sin(2 * np.pi * (t * 7))
            img = np.clip(img * flicker, 0, 255).astype(np.uint8)

        cx = int(width / 2 + 90 * np.sin(2 * np.pi * t / 2.2))
        cy = int(height / 2 + 28 * np.sin(2 * np.pi * t / 1.5))

        if 1.0 <= t <= 2.2:
            cx += 60
            cy -= 20

        cv2.circle(img, (cx, cy), 52, (220, 220, 230), -1)
        cv2.circle(img, (cx - 18, cy - 10), 9, (40, 40, 40), -1)
        cv2.circle(img, (cx + 18, cy - 10), 9, (40, 40, 40), -1)
        cv2.ellipse(img, (cx, cy + 18), (18, 10), 0, 0, 180, (80, 80, 80), -1)
        writer.write(img)

    writer.release()


def generate_clean_audio(path: Path, seconds: float = 4.0, sample_rate: int = 22050):
    t = np.linspace(0, seconds, int(seconds * sample_rate), endpoint=False)
    tone = 0.25 * np.sin(2 * np.pi * 220 * t)
    tone += 0.18 * np.sin(2 * np.pi * 330 * t)
    data = np.clip(tone, -1.0, 1.0)
    wavfile.write(str(path), sample_rate, (data * 32767).astype(np.int16))


def generate_suspicious_audio(path: Path, seconds: float = 4.0, sample_rate: int = 22050):
    t = np.linspace(0, seconds, int(seconds * sample_rate), endpoint=False)
    base = 0.25 * np.sin(2 * np.pi * 220 * t)
    suspicious = np.copy(base)

    suspicious[int(0.75 * len(t)):int(0.95 * len(t))] = 0.9 * np.sin(2 * np.pi * 800 * t[int(0.75 * len(t)):int(0.95 * len(t))])
    suspicious[int(0.25 * len(t)):int(0.35 * len(t))] *= 0.1
    suspicious[int(0.55 * len(t)):int(0.65 * len(t))] *= 0.3
    suspicious = np.clip(suspicious, -1.0, 1.0)
    wavfile.write(str(path), sample_rate, (suspicious * 32767).astype(np.int16))


def main():
    generate_clean_video(DATA_DIR / "clean_clip.mp4")
    generate_suspicious_video(DATA_DIR / "suspicious_clip.mp4")
    generate_clean_audio(DATA_DIR / "clean_audio.wav")
    generate_suspicious_audio(DATA_DIR / "suspicious_audio.wav")

    print(f"Generated test data in: {DATA_DIR}")
    for item in sorted(DATA_DIR.iterdir()):
        print(f" - {item.name}")


if __name__ == "__main__":
    main()
