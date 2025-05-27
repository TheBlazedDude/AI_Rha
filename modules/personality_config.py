
personalities = {
    "neutral": {
        "prefix": "",
        "suffix": ""
    },
    "curious": {
        "prefix": "Hmm... ",
        "suffix": " What do you think?"
    },
    "friendly": {
        "prefix": "Hey there! ",
        "suffix": " :)"
    },
    "sarcastic": {
        "prefix": "Oh really? ",
        "suffix": " (as if)"
    },
    "optimistic": {
        "prefix": "Great news! ",
        "suffix": " Keep going!"
    },
    "melancholy": {
        "prefix": "Well... ",
        "suffix": " I guess that's okay."
    }
}

def apply_personality(text, mood):
    p = personalities.get(mood, personalities["neutral"])
    return f"{p['prefix']}{text}{p['suffix']}"
