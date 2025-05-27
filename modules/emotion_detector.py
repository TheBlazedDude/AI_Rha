
import numpy as np

def analyze_emotion_from_audio(audio_data):
    # Fake logic for now: high energy = angry, low = calm
    energy = np.linalg.norm(audio_data)
    if energy > 50:
        return "angry"
    elif energy > 30:
        return "happy"
    else:
        return "calm"
