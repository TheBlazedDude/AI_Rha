
import json
from datetime import datetime
import os

def log_interaction(input_type, content, emotion=None, tone=None):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "input_type": input_type,
        "content": content,
        "emotion": emotion,
        "tone": tone
    }
    path = "data/memory_timeline.json"
    memory = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            memory = json.load(f)
    memory.append(entry)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)
