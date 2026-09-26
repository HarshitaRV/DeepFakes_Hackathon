import numpy as np
from scipy.io import wavfile

from ml_pipeline import extract_feature_vector, train_classifier


def test_extract_feature_vector_returns_fixed_length_vector(tmp_path):
    audio_path = tmp_path / "demo.wav"
    sr = 16000
    t = np.linspace(0, 1, sr, endpoint=False)
    signal = 0.2 * np.sin(2 * np.pi * 220 * t)
    wavfile.write(str(audio_path), sr, (signal * 32767).astype(np.int16))

    vector = extract_feature_vector(str(audio_path))

    assert vector.shape == (40,)
    assert np.isfinite(vector).all()


def test_train_classifier_succeeds_on_synthetic_audio(tmp_path):
    train_dir = tmp_path / "train"
    real_dir = train_dir / "real"
    fake_dir = train_dir / "fake"
    real_dir.mkdir(parents=True)
    fake_dir.mkdir(parents=True)

    sr = 16000
    for i in range(4):
        t = np.linspace(0, 1, sr, endpoint=False)
        tone = 0.3 * np.sin(2 * np.pi * (220 + i * 10) * t)
        wavfile.write(str(real_dir / f"real_{i}.wav"), sr, (tone * 32767).astype(np.int16))

        mod = tone * (1.0 + 0.4 * np.sin(2 * np.pi * 8 * t))
        wavfile.write(str(fake_dir / f"fake_{i}.wav"), sr, (mod * 32767).astype(np.int16))

    model, metrics = train_classifier(str(train_dir), out_dir=str(tmp_path))

    assert model is not None
    assert metrics["accuracy"] >= 0.0
    assert "confusion_matrix" in metrics
