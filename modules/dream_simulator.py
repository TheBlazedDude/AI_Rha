
import json
from datetime import datetime

def summarize_day():
    try:
        with open("data/reflection_log.json", "r", encoding="utf-8") as f:
            reflections = json.load(f)
    except:
        print("No reflections found.")
        return "I haven't experienced anything yet..."

    if not reflections:
        return "Today was quiet."

    dreams = ["In my dream, I remembered...\n"]
    for item in reflections[-5:]:  # last 5 entries
        dreams.append(f"{item['timestamp'][:10]}: '{item['trigger']}' → '{item['response']}' (felt {item['emotion']}, confidence {item['confidence']:.2f})")
    return "\n".join(dreams)
