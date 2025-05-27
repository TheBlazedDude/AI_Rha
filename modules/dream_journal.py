
import json
from datetime import datetime

def log_dream_entry(summary):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "summary": summary
    }
    path = "data/dream_journal.json"
    journal = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            journal = json.load(f)
    except:
        pass
    journal.append(entry)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(journal, f, indent=2)

def get_recent_dreams(limit=5):
    try:
        with open("data/dream_journal.json", "r", encoding="utf-8") as f:
            entries = json.load(f)
        return "\n".join([f"{i+1}. {e['timestamp'][:19]}: {e['summary']}" for i, e in enumerate(entries[-limit:])])
    except:
        return "No dreams recorded yet."

def edit_dream(index, new_summary):
    try:
        with open("data/dream_journal.json", "r", encoding="utf-8") as f:
            entries = json.load(f)
        if 0 <= index < len(entries):
            entries[index]["summary"] = new_summary
            with open("data/dream_journal.json", "w", encoding="utf-8") as f:
                json.dump(entries, f, indent=2)
            return "Dream updated."
        else:
            return "Invalid index."
    except:
        return "Failed to update dream."
