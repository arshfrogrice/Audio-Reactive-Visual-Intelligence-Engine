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

        data = analyze_audio(song,duration=60)

        features.append(
            extract_features(data)
        )

    model = KMeans(
        n_clusters=3,
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

    mood_map = {
    0: "Energetic",
    1: "Calm",
    2: "Balanced"
    }   

    return mood_map[cluster]