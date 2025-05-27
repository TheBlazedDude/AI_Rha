
from ai_core.memory import load_knowledge, save_word, save_sentence
from datetime import datetime
import os

def ask_for_word_info(word):
    word = word.lower()
    print(f"AI: I don't know the word '{word}'. Let's learn it together.")

    def ask_list(prompt):
        print(prompt + " (leave empty to skip or type multiple separated by commas):")
        value = input()
        return [item.strip() for item in value.split(",") if item.strip()] if value else []

    def ask_string(prompt):
        print(prompt + " (leave empty to skip):")
        return input().strip()

    def ask_dict(prompt_keys):
        d = {}
        for key in prompt_keys:
            val = ask_string(f"Enter {key} form")
            if val:
                d[key] = val
        return d

    meanings = ask_list("Meanings")
    word_types = ask_list("Types (noun, verb, adjective, etc.)")
    synonyms = ask_list("Synonyms")
    antonyms = ask_list("Antonyms")

    examples = []
    print("Example sentences (press Enter without typing to stop):")
    while True:
        ex = input("Example: ").strip()
        if not ex:
            break
        examples.append(ex)

    tenses = ask_dict(["past", "present", "future"])

    pronunciation = ask_string("Pronunciation (e.g., /kæt/)")
    root = ask_string("Root/Base form")
    language = ask_string("Language")
    morphology = ask_list("Morphology parts (e.g., un-, believe, -able)")
    usage_contexts = ask_list("Usage contexts (e.g., informal, slang)")
    related_words = ask_list("Related words")
    associated_concepts = ask_list("Associated concepts")
    emotion_tone = ask_list("Emotion tone (e.g., happy, sad)")
    grammar_notes = ask_string("Any grammar notes")
    audio_reference = ask_string("Audio file path")
    visual_reference = ask_string("Visual image path")

    entry = {
        "meaning": meanings,
        "type": word_types,
        "synonyms": synonyms,
        "antonyms": antonyms,
        "examples": examples,
        "tenses": tenses,
        "pronunciation": pronunciation,
        "root": root,
        "language": language,
        "morphology": morphology,
        "usage_contexts": usage_contexts,
        "related_words": related_words,
        "associated_concepts": associated_concepts,
        "emotion_tone": emotion_tone,
        "grammar_notes": grammar_notes,
        "audio_reference": audio_reference,
        "visual_reference": visual_reference,
        "learned_from": "user",
        "timestamp": datetime.now().isoformat()
    }

    save_word(word, entry)

def learn_sentence(sentence):
    knowledge = load_knowledge()
    words = sentence.strip().split()
    known_words = knowledge["words"]

    print("AI: Let me check these words...")

    for word in words:
        if word.lower() not in known_words:
            ask_for_word_info(word.lower())

    sentence_meaning = input("What do the words together mean in this sentence? ")
    sentence_entry = {
        "text": sentence,
        "words": words,
        "meaning": sentence_meaning,
        "timestamp": datetime.now().isoformat()
    }

    save_sentence(sentence_entry)
