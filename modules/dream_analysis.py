import os


def get_dream_menu():
    return (
        "\nI'm in a dream. You can now:\n"
        "1. Review recent memory (chat/audio/vision logs)\n"
        "2. See frequent responses\n"
        "3. Analyze common triggers\n"
        "4. Check confidence trends\n"
        "5. Summarize emotional tone\n"
        "Type a number to continue or 'wake up' to exit.\n"
    )

def analyze_responses():
    import json
    from collections import Counter
    path = "data/responses.json"
    if not os.path.exists(path): return "No responses recorded yet."
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    most_frequent = sorted(data.items(), key=lambda x: len(x[1]), reverse=True)[:5]
    return "\n".join([f"{k} → {len(v)} variants" for k, v in most_frequent])

def analyze_memory():
    import json
    path = "data/memory_timeline.json"
    if not os.path.exists(path): return "No memory timeline found."
    with open(path, "r", encoding="utf-8") as f:
        entries = json.load(f)[-5:]
    return "\n".join([f"{e['timestamp'][:19]} [{e['input_type']}] → {e['content']}" for e in entries])

def analyze_triggers():
    import json
    from collections import Counter
    path = "data/responses.json"
    if not os.path.exists(path): return "No triggers recorded yet."
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return f"Total unique triggers: {len(data)}"

def analyze_confidence():
    import json
    path = "data/reflection_log.json"
    if not os.path.exists(path): return "No reflection log found."
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not data: return "No confidence entries found."
    scores = [entry["confidence"] for entry in data if "confidence" in entry]
    avg = sum(scores) / len(scores)
    return f"Average confidence: {avg:.2f} (based on {len(scores)} responses)"

def analyze_emotions():
    import json
    from collections import Counter
    path = "data/reflection_log.json"
    if not os.path.exists(path): return "No reflection log found."
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    emotions = [entry.get("emotion", "neutral") for entry in data]
    count = Counter(emotions)
    return "\n".join([f"{k}: {v}" for k, v in count.items()])
