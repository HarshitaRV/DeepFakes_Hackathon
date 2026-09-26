# Data directory

Use this folder to store a small real-world deepfake audio dataset for training and evaluation.

Recommended structure:

```text
data/
  real/
    audio_001.wav
    audio_002.wav
  fake/
    audio_101.wav
    audio_102.wav
```

This repo keeps the synthetic files in test_data/ as smoke tests only.
The real ML pipeline expects a dataset split under data/ with `real/` and `fake/` folders.
