from pathlib import Path

import numpy as np
from scipy.io import wavfile


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "test_data"
DATA_DIR.mkdir(exist_ok=True)


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
    generate_clean_audio(DATA_DIR / "clean_audio.wav")
    generate_suspicious_audio(DATA_DIR / "suspicious_audio.wav")

    print(f"Generated audio test data in: {DATA_DIR}")
    for item in sorted(DATA_DIR.iterdir()):
        print(f" - {item.name}")


if __name__ == "__main__":
    main()
