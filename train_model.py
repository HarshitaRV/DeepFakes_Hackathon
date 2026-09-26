import argparse

from ml_pipeline import train_classifier


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a lightweight audio deepfake classifier.")
    parser.add_argument("--dataset", type=str, default="data", help="Directory with real/ and fake/ folders")
    parser.add_argument("--out-dir", type=str, default="artifacts", help="Directory for model and metrics")
    args = parser.parse_args()

    model, metrics = train_classifier(args.dataset, args.out_dir)
    print(f"Model trained successfully: {model.__class__.__name__}")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"F1: {metrics['f1']:.4f}")
    print(f"Confusion matrix: {metrics['confusion_matrix']}")
