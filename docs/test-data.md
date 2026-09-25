# Test Data for the Hackathon Prototype

## What is included
This project now includes a small synthetic dataset for validating both success and failure scenarios.

### Files generated into test_data/
- clean_clip.mp4: expected negative case, low anomaly
- suspicious_clip.mp4: expected positive case, visual inconsistencies and flicker
- clean_audio.wav: expected negative audio case
- suspicious_audio.wav: expected positive audio anomaly case

## Why synthetic data is useful here
For a one-day hackathon, synthetic data is the fastest way to validate:
- the upload pipeline works
- suspicious segments are identified
- clean samples do not trigger false positives
- the explainable report is meaningful

## Validation expectations

### Negative / success case
- clean_clip.mp4 should not trigger strong video anomaly warnings
- clean_audio.wav should not trigger strong audio anomaly warnings

### Positive / failure case
- suspicious_clip.mp4 should trigger visual inconsistency warnings
- suspicious_audio.wav should trigger suspicious audio windows

## Regenerate data
```bash
python scripts/generate_test_media.py
```
