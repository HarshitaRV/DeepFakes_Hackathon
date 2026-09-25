# Local Prototype Stack and Run Commands

## Recommended stack
This is the simplest stack that is realistic for a 1-day hackathon and runs locally on a laptop.

- Frontend: Streamlit
- Backend: Python app layer
- Video processing: OpenCV
- Audio processing: librosa + scipy
- Metadata/provenance: ffprobe + basic file metadata parsing
- Local environment: Python virtual environment

## Python package list
Create a file named requirements.txt with this content:

```txt
numpy==2.5.3
opencv-python-headless==4.10.0.84
scipy==1.18.1
librosa==1.0.0
pillow==11.3.0
streamlit==1.64.0
python-multipart==0.0.20
mutagen==1.47.0
```

## Install FFmpeg on macOS
If ffprobe or FFmpeg is not already available:

```bash
brew install ffmpeg
```

## Local setup commands
Run these from the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the app
Start the app locally:

```bash
streamlit run app.py --server.port 8501
```

Open in browser:
- http://localhost:8501

## Optional quick validation command
Check imports before launching the app:

```bash
python -c "import streamlit, cv2, librosa, numpy, PIL, mutagen; print('imports ok')"
```

## MVP app behavior
The app should:
- allow upload of a local video file
- display basic file details
- estimate suspicious frame ranges based on visual inconsistency
- estimate suspicious audio time ranges based on signal variance
- produce a human-readable summary with risk tier
- recommend human review

## Example risk output
```text
Face and audio inconsistencies detected.
Video suspicion: frames 140–190.
Audio suspicion: 0:18–0:24.
No clear provenance chain found.
Risk tier: Medium.
Recommended action: Human review.
```

This keeps the prototype aligned with the project goal without claiming a definitive authenticity verdict.
