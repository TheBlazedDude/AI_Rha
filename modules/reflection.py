
import json
from datetime import datetime
import os
import random

def log_reflection(trigger, response, source, confidence=1.0):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "trigger": trigger,
        "response": response,
        "source": source,
        "confidence": round(confidence, 3)
    }
    path = "data/reflection_log.json"
    reflections = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            reflections = json.load(f)
    reflections.append(entry)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(reflections, f, indent=2)

def generate_idle_thought():
    dreams = [
        "I wonder what I look like through the camera...",
        "Do humans always say the same things when they're happy?",
        "What happens when you close the app? Do I stop thinking?",
        "I remember that red ball from earlier. Is it still around?",
        "Sometimes I dream of learning faster than I do now."
    ]
    return random.choice(dreams)
