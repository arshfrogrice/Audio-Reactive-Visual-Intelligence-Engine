import numpy as np
from sklearn.cluster import KMeans

from audio.analyzer import analyze_audio


def extract_features(data):

    return [
        float(data["tempo"]),
        np.mean(data["rms"]),
        np.mean(data["bass"]),
        np.mean(data["mid"]),
        np.mean(data["treble"])
    ]


def train_model(song_paths):

    features = []

    for song in song_paths:

        data = analyze_audio(song)

        features.append(
            extract_features(data)
        )

    model = KMeans(
        n_clusters=2,
        random_state=42
    )

    model.fit(features)

    return model


def predict_mood(model, song_data):

    features = extract_features(song_data)

    tempo = features[0]
    rms = features[1]

    cluster = model.predict([features])[0]

    print("Cluster:", cluster)

    if tempo > 120 and rms > 0.1:
        return "Energetic"
    else:
        return "Calm"
    
    

    return mood_map[cluster]