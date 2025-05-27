
import json
from datetime import datetime, timedelta

def search_memory(query):
    path = "data/memory_timeline.json"
    if not query.strip(): return "Empty query."
    try:
        with open(path, "r", encoding="utf-8") as f:
            entries = json.load(f)
        results = []
        for e in entries[-50:]:
            if query.lower() in e["content"].lower():
                results.append(f"{e['timestamp'][:19]} → {e['content']}")
        return "\n".join(results) if results else "No memory found for that query."
    except:
        return "Memory access failed."
