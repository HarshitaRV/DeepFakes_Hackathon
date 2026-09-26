import argparse
import pickle
from pathlib import Path

from ml_pipeline import load_dataset, extract_feature_vector


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate a trained audio classifier.")
    parser.add_argument("--dataset", type=str, default="data", help="Directory with real/ and fake/ folders")
    parser.add_argument("--model", type=str, default="artifacts/audio_classifier.pkl", help="Saved model path")
    args = parser.parse_args()

    with open(args.model, "rb") as f:
        model = pickle.load(f)

    X, y = load_dataset(args.dataset)
    preds = model.predict(X)
    acc = (preds == y).mean()
    print(f"Evaluation accuracy: {acc:.4f}")
    print(f"Correct predictions: {int((preds == y).sum())}/{len(y)}")
