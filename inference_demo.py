import argparse
import pickle

from ml_pipeline import extract_feature_vector


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run audio inference with the trained model.")
    parser.add_argument("--audio", type=str, required=True, help="Path to an audio file")
    parser.add_argument("--model", type=str, default="artifacts/audio_classifier.pkl", help="Saved model path")
    args = parser.parse_args()

    with open(args.model, "rb") as f:
        model = pickle.load(f)

    features = extract_feature_vector(args.audio)
    prediction = model.predict([features])[0]
    label = "real" if prediction == 1 else "fake"
    print(f"Prediction: {label}")
