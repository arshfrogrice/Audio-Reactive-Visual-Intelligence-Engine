import librosa
import numpy as np

def analyze_audio(file_path,duration=None):
    y, sr = librosa.load(file_path, sr=22050,duration=duration)
    
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)    
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    
    
    #stft analysis
    stft = librosa.stft(y)
    spectrogram = np.abs(stft)
    freqs = librosa.fft_frequencies(sr=sr)

    bass_mask = (freqs >=20) & (freqs < 250)    
    bass_energy = np.mean(spectrogram[bass_mask, :], axis=0)
    
    mid_mask = (freqs >= 250) & (freqs < 4000)  
    mid_energy = np.mean(spectrogram[mid_mask, :], axis=0)
    
    treble_mask =  freqs >= 4000
    treble_energy = np.mean(spectrogram[treble_mask, :], axis=0)
    
    freq_times = librosa.times_like(bass_energy, sr=sr) 
    
    #rms energy
    rms = librosa.feature.rms(y=y)[0]
    rms_times = librosa.times_like(rms, sr=sr)

    return {
        "tempo": float(tempo[0]) if hasattr(tempo, "__len__") else float(tempo),
        "beat_times": beat_times,
        "rms": rms,
        "rms_times": rms_times,
        "bass": bass_energy,
        "mid": mid_energy,
        "treble": treble_energy,
        "freq_times": freq_times
    }

