import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "deepfake-forensics 2" / "backend"))

import main


def test_plain_summary_creates_short_sentence_for_detected_video_signal():
    summary = main.generate_plain_summary(
        [{"start": 4.2, "end": 9.8, "type": "face"}],
        [],
        {"c2pa_found": False, "note": "No provenance found"},
    )

    assert "Face region shows manipulation artifacts from 4.2s to 9.8s." in summary
    assert "No content provenance found." in summary


def test_build_response_includes_summary_and_ranges():
    response = main.build_response(
        "demo-id",
        [{"time": 0.0, "confidence": 0.1}, {"time": 1.0, "confidence": 0.9}],
        [{"start": 0.0, "end": 1.0, "type": "face"}],
        [{"start": 2.0, "end": 3.0, "type": "audio", "note": "voice mismatch"}],
        {"c2pa_found": True, "note": "Found provenance"},
    )

    assert response["summary_sentence"]
    assert response["provenance_line"]
    assert response["flagged_ranges"][0]["kind"] in {"video", "audio"}
