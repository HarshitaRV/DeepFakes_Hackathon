import json
import pickle
from pathlib import Path

import librosa
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split


FEATURE_DIM = 40


def extract_feature_vector(audio_path: str):
    y, sr = librosa.load(audio_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    delta = librosa.feature.delta(mfcc)
    feature = np.concatenate([
        mfcc.mean(axis=1),
        mfcc.std(axis=1),
        delta.mean(axis=1),
        delta.std(axis=1),
    ])
    if feature.size < FEATURE_DIM:
        pad = np.zeros(FEATURE_DIM - feature.size)
        feature = np.concatenate([feature, pad])
    return feature[:FEATURE_DIM].astype(np.float32)


def load_dataset(dataset_dir: str):
    dataset_path = Path(dataset_dir)
    X = []
    y = []

    for label_dir in ["real", "fake"]:
        label = 1 if label_dir == "real" else 0
        class_dir = dataset_path / label_dir
        if not class_dir.exists():
            continue
        for audio_file in sorted(class_dir.glob("*.wav")):
            X.append(extract_feature_vector(str(audio_file)))
            y.append(label)

    if not X:
        raise ValueError(f"No audio files found in dataset directory: {dataset_dir}")

    return np.vstack(X), np.array(y, dtype=int)


def train_classifier(dataset_dir: str, out_dir: str = "artifacts"):
    X, y = load_dataset(dataset_dir)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    metrics = {
        "accuracy": float(accuracy_score(y_test, preds)),
        "f1": float(f1_score(y_test, preds, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_test, preds).tolist(),
    }

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    with open(out_path / "audio_classifier.pkl", "wb") as f:
        pickle.dump(model, f)
    with open(out_path / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    return model, metrics
