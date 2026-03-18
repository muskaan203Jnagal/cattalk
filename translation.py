import pandas as pd
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_translations():
    path = os.path.join(BASE_DIR, "data", "translations.csv")
    df = pd.read_csv(path)
    return df.set_index("sound_key").to_dict(orient="index")

def load_mood_map():
    path = os.path.join(BASE_DIR, "data", "mood_map.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

TRANSLATIONS = load_translations()
MOOD_MAP     = load_mood_map()

# Human keywords → cat response
HUMAN_RESPONSES = {
    "hungry" : "Okay okay aa rahi hoon! Khana de rahi hoon! 🍜",
    "food"   : "Khana aa gaya! Khao meri jaan! 🐟",
    "eat"    : "Lo khao! Meri pyaari billi! 🥣",
    "hello"  : "Hello meri pyaari billi! Kaisi ho? 🥰",
    "hi"     : "Heyyy cutie pie! 😄",
    "love"   : "I love you too my little furball! 💕",
    "play"   : "Chalo khelein! Toy laati hoon! 🎾",
    "sleep"  : "Okay soja, disturb nahi karungi! 🌙",
    "good"   : "You are such a good cat! 🌟",
    "bad"    : "Sorry baby, galti ho gayi! Maaf karo! 🙏",
    "come"   : "Idhar aao meri jaan! 🤗",
    "go"     : "Okay okay, jaati hoon! 😅",
    "water"  : "Lo paani! Fresh aur thanda! 💧",
    "bath"   : "Nahi nahi nahi! Please nahi! 😱",
    "vet"    : "Nahi! Wahan nahi jaana! Mujhe mat le jao! 😰",
    "treat"  : "TREAT?! Kahan hai?! Abhi do! 🎉",
    "brush"  : "Hmm... theek hai, thoda achha lagta hai! 😌",
    "outside": "HAAN! Bahar jaana hai! Door kholo! 🌿",
    "inside" : "Okay andar aa jaati hoon... 🏠",
    "no"     : "Tum mujhe rok nahi sakte! Main billi hoon! 😤",
    "yes"    : "Obviously! Main toh pehle se jaanti thi! 😏",
}

def get_cat_translation(sound_key, lang="en"):
    if sound_key not in TRANSLATIONS:
        return {
            "text"  : "Meow? (Unknown sound)",
            "mood"  : "Unknown",
            "emoji" : "🐱",
            "pct"   : 50,
            "color" : "gray"
        }
    t = TRANSLATIONS[sound_key]
    m = MOOD_MAP.get(sound_key, {})
    text = t["human_translation_hi"] if lang == "hi" else t["human_translation_en"]
    return {
        "text"    : text,
        "meaning" : t["meaning"],
        "context" : t["context"],
        "mood"    : m.get("mood", "Unknown"),
        "emoji"   : m.get("emoji", "🐱"),
        "pct"     : m.get("pct", 50),
        "color"   : m.get("color", "gray")
    }

def get_human_response(user_text):
    user_lower = user_text.lower()
    for keyword, response in HUMAN_RESPONSES.items():
        if keyword in user_lower:
            return response
    return "Meow? 🐱 (Cat is listening and thinking...)"

def get_all_sounds():
    return {k: v for k, v in TRANSLATIONS.items()}
