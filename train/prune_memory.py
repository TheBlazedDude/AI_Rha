
import json

def prune_responses(threshold=0.4):
    path = "data/responses.json"
    with open(path, "r", encoding="utf-8") as f:
        responses = json.load(f)

    cleaned = {}
    for k, items in responses.items():
        if isinstance(items, list):
            filtered = [resp for resp in items if resp.get("score", 0.5) >= threshold]
            if filtered:
                cleaned[k] = filtered
        else:
            if items.get("score", 0.5) >= threshold:
                cleaned[k] = [items]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2)
    print(f"Pruned low-confidence responses. {len(cleaned)} keys remain.")
