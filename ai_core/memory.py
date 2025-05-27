
import json
import os

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_knowledge():
    return {
        "alphabet": load_json("data/alphabet.json"),
        "numbers": load_json("data/numbers.json"),
        "symbols": load_json("data/symbols.json"),
        "words": load_json("data/words.json")
    }

def save_word(word, entry):
    word = word.lower()
    data = load_json("data/words.json")
    data[word] = entry
    save_json("data/words.json", data)

def save_sentence(sentence_entry):
    path = "data/sentences.json"
    data = load_json(path)
    if not isinstance(data, list):
        data = []
    data.append(sentence_entry)
    save_json(path, data)
