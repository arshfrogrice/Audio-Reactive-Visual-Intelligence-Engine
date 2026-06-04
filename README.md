# 🎵 Pulse: An Audio-Reactive Visual Intelligence Engine

A multimedia performance system that analyzes audio and transforms it into dynamic, interactive visuals using **digital signal processing**, **machine learning**, and **procedural graphics**.

---

## Demo

> Particle systems, flow fields, and network connections respond live to beat timing, bass energy, and frequency bands — with mood automatically detected by a trained KMeans classifier.

---

## Architecture

```
┌─────────────────────┐     ┌──────────────────────┐
│   audio/            │     │   ml/                │
│   analyzer.py       │────▶│   mood_classifier.py │
│                     │     │                      │
│  librosa + NumPy    │     │  scikit-learn KMeans │
│  FFT / STFT         │     │  feature → preset    │
└────────┬────────────┘     └──────────┬───────────┘
         │                             │
         └─────────────┬───────────────┘
                       ▼
            ┌──────────────────────┐
            │   main.py            │
            │   Pygame renderer    │
            │   particle system    │
            │   flow fields        │
            │   beat-sync pulses   │
            └──────────────────────┘
```

---

## Features

**Audio Analysis (`audio/analyzer.py`)**
- Loads audio via librosa at 22050 Hz (configurable)
- Accepts an optional `duration` parameter to analyze only the first N seconds — used during training to speed up feature extraction across large song libraries
- Extracts tempo and beat frame timestamps using `librosa.beat.beat_track`
- Computes STFT and splits the spectrogram into three frequency bands:
  - **Bass** (20–250 Hz) → drives particle force and beat-pulse intensity
  - **Mid** (250–4000 Hz) → controls flow-field strength and turbulence
  - **Treble** (4000+ Hz) → controls connection-line brightness and sharpness
- Computes per-frame RMS energy for overall amplitude mapping

**Mood Classification (`ml/mood_classifier.py`)**
- Extracts a 5-feature vector per song: tempo, avg RMS, avg bass, avg mid, avg treble
- During training, each song is analyzed with `duration=60` (first 60 seconds) for faster processing
- Trains a KMeans model with **3 clusters** on a library of songs
- Predicts mood at startup and selects a matching visual preset:
  - **Energetic** — high particle count (80), bright pink/purple palette, strong forces, intense flash
  - **Calm** — fewer particles (60), soft blue palette, gentle flow, subtle trail
  - **Balanced** — medium particle count (70), violet/periwinkle palette, moderate flow, blue-tinted flash

**Procedural Renderer (`main.py`)**
- Pygame-based particle system with per-particle velocity and flow-field steering
- Particles respond to beat events with velocity impulses proportional to bass energy
- Sine/cosine noise field warps particle trajectories over time
- Proximity-based connection lines drawn between nearby particles, colored by treble intensity
- Exponential smoothing on all frequency bands to prevent visual flickering
- Fade surface creates motion-trail persistence effect
- Flash color on beat is mood-aware: pink for Energetic, indigo for Balanced, teal for Calm

---

## Tech Stack

| Domain | Libraries |
|---|---|
| Audio analysis | `librosa`, `numpy` |
| Machine learning | `scikit-learn` |
| Rendering | `pygame` |
| Audio playback | `pygame.mixer` |

---

## Project Structure

```
Audio-Reactive-Visual-Intelligence-Engine/
│
├── main.py                  # Entry point — renderer and main loop
│
├── audio/
│   ├── __init__.py
│   └── analyzer.py          # FFT/STFT analysis, beat tracking, band energy
│
├── ml/
│   ├── __init__.py
│   └── mood_classifier.py   # KMeans mood classification + visual preset selection
│
└── audio/                   # Training songs directory (not tracked by git)
    └── *.mp3
```

---

## Setup

**Requirements: Python 3.9+**

```bash
git clone https://github.com/arshfrogrice/Audio-Reactive-Visual-Intelligence-Engine.git
cd Audio-Reactive-Visual-Intelligence-Engine
pip install librosa numpy scikit-learn pygame
```

---

## Usage

**Step 1 — Train the mood classifier**

Edit the `training_songs` list in `main.py` (or run `ml/mood_classifier.py` directly) to point to audio files on your machine. Aim for variety — include energetic, ambient, calm, and balanced tracks for cleaner clusters. Each song is analyzed using only its first 60 seconds for faster training.

```bash
python -c "
from ml.mood_classifier import train_model
songs = ['path/to/song1.mp3', 'path/to/song2.mp3']  # add 8-15+ songs
train_model(songs)
"
```

**Step 2 — Run the engine**

Edit the `song` variable in `main.py` to point to your target audio file, then:

```bash
python main.py
```

The system will:
1. Analyze the song (takes a few seconds for STFT)
2. Print detected tempo and beat timestamps
3. Predict mood and print `Detected Mood: Energetic` (or Calm, or Balanced)
4. Launch the Pygame window and begin playback with synchronized visuals

---

## How the Audio-Visual Mapping Works

```
Beat detected
    └─▶ velocity impulse on all particles  (magnitude ∝ bass energy)
    └─▶ mood-colored screen flash          (pink / indigo / teal)

Bass energy (smooth)
    └─▶ particle speed multiplier + beat-pulse radius

Mid energy (smooth)
    └─▶ flow-field sine/cosine warp strength

Treble energy (smooth)
    └─▶ connection-line color intensity  (line_intensity = 100 + treble × 40)

RMS energy (per frame)
    └─▶ particle draw radius  (size + pulse + rms × 8)
```

Exponential smoothing (`α = 0.1`) is applied to all band energies each frame to prevent abrupt visual jumps from transient spikes.

---

## Mood Presets

| Mood | Particles | Trail Alpha | Palette | Flash Color |
|---|---|---|---|---|
| **Energetic** | 80 | 35 | Pink / violet | `(80, 20, 80)` |
| **Calm** | 60 | 20 | Sky blue / cyan | `(20, 60, 80)` |
| **Balanced** | 70 | 30 | Periwinkle / lavender | `(50, 40, 80)` |

---

## Key Concepts Demonstrated

- **Short-Time Fourier Transform (STFT)** — frequency decomposition over sliding time windows, giving time-varying spectral information rather than a single global FFT
- **Frequency bin masking** — isolating bass/mid/treble by selecting rows of the spectrogram corresponding to target Hz ranges
- **Beat tracking** — autocorrelation-based onset detection via librosa, converted to timestamps for frame-accurate pulse triggering
- **Unsupervised learning** — KMeans clustering (3 clusters) on audio feature vectors to group songs by character without labelled training data
- **Flow-field steering** — per-particle velocity nudging via a 2D sine/cosine noise field, creating organic swirling motion independent of audio

---

## Extending the Project

- **Add more moods** — increase `n_clusters` in `mood_classifier.py` and retrain on a larger song library; inspect cluster centroids to assign labels
- **MediaPipe gesture control** — real-time interaction and preset switching
- **Live microphone input** — replace `pygame.mixer` playback + pre-analyzed data with a `sounddevice` stream feeding librosa's streaming STFT for true real-time processing
- **Shader effects** — replace Pygame's software renderer with ModernGL for GPU-accelerated particle rendering and GLSL shaders

---

## License

MIT License — see `LICENSE` for details.
