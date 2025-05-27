
import json
from datetime import datetime

def generate_day_summary():
    try:
        with open("data/memory_timeline.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        return "No memory recorded today."

    today = datetime.now().strftime("%Y-%m-%d")
    today_data = [e for e in data if e["timestamp"].startswith(today)]

    if not today_data:
        return "I didn't experience anything today."

    lines = [f"{e['timestamp'][11:19]} [{e['input_type']}] → {e['content']}" for e in today_data]
    return "Today I experienced:" + "".join(lines)
