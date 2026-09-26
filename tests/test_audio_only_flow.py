import numpy as np
from scipy.io import wavfile

from app import build_audio_report, extract_basic_audio_metadata


def test_extract_basic_audio_metadata_reads_audio_file(tmp_path):
    audio_path = tmp_path / "demo.wav"
    sr = 22050
    t = np.linspace(0, 2, int(2 * sr), endpoint=False)
    tone = 0.25 * np.sin(2 * np.pi * 220 * t)
    wavfile.write(str(audio_path), sr, (tone * 32767).astype(np.int16))

    metadata = extract_basic_audio_metadata(str(audio_path))

    assert metadata["kind"] == "audio"
    assert metadata["duration_seconds"] > 0
    assert metadata["source"] == "local upload"


def test_build_audio_report_focuses_on_audio_only():
    metadata = {
        "duration_seconds": 2.0,
        "source": "local upload",
        "provenance": "No clear provenance chain detected",
    }
    audio_anomaly = {
        "status": "Suspicious audio discontinuities detected",
        "suspicious_windows": [{"start": 0.5, "end": 1.1}],
    }

    report = build_audio_report(metadata, audio_anomaly)

    assert "audio" in report.lower()
    assert "0.5s" in report
    assert "1.1s" in report
