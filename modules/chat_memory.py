
import os

def last_seen():
    vision_files = sorted(os.listdir("data/vision_log"))
    if vision_files:
        last_vision = vision_files[-1]
        with open(f"data/vision_log/{last_vision}", "r") as f:
            label = f.read().strip()
        return f"Last thing I saw: {label}"
    else:
        return "I haven't seen anything yet."

def last_heard():
    audio_files = sorted([f for f in os.listdir("data/audio") if f.endswith(".txt")])
    if audio_files:
        last_audio = audio_files[-1]
        with open(f"data/audio/{last_audio}", "r") as f:
            text = f.read().strip()
        return f"Last thing I heard: {text}"
    else:
        return "I haven't heard anything yet."

if __name__ == "__main__":
    print(last_seen())
    print(last_heard())
