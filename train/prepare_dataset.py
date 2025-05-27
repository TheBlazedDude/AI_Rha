
import os
import json

def build_training_data():
    response_path = "data/responses.json"
    vision_path = "data/vision_log"
    audio_path = "data/audio"

    samples = []
    if os.path.exists(response_path):
        with open(response_path, "r", encoding="utf-8") as f:
            responses = json.load(f)

        for key, items in responses.items():
            if isinstance(items, list):
                for item in items:
                    entry = {
                        "prompt": key,
                        "response": item["text"],
                        "score": item.get("score", 0.5)
                    }
                    samples.append(entry)

    with open("../data/training_dataset.json", "w", encoding="utf-8") as f:
        json.dump(samples, f, indent=2)

    print(f"Prepared {len(samples)} prompt-response training samples.")

if __name__ == "__main__":
    build_training_data()
