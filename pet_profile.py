import json
import os

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
PROFILES_FILE = os.path.join(BASE_DIR, "data", "pet_profiles.json")

def load_profiles():
    if not os.path.exists(PROFILES_FILE):
        return {}
    with open(PROFILES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_profiles(profiles):
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)

def add_profile(name, breed, age, about=""):
    profiles = load_profiles()
    profiles[name] = {
        "name"        : name,
        "breed"       : breed,
        "age"         : age,
        "about"       : about,
        "mood_history": [],
        "total_chats" : 0
    }
    save_profiles(profiles)

def get_profile(name):
    profiles = load_profiles()
    return profiles.get(name)

def update_mood_history(name, mood):
    profiles = load_profiles()
    if name in profiles:
        profiles[name]["mood_history"].append(mood)
        profiles[name]["total_chats"] += 1
        save_profiles(profiles)

def get_all_profile_names():
    return list(load_profiles().keys())

def delete_profile(name):
    profiles = load_profiles()
    if name in profiles:
        del profiles[name]
        save_profiles(profiles)

def get_most_common_mood(name):
    profile = get_profile(name)
    if not profile or not profile["mood_history"]:
        return "No data yet"
    from collections import Counter
    return Counter(profile["mood_history"]).most_common(1)[0][0]
