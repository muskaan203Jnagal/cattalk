import json
import os
from datetime import datetime

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR  = os.path.join(BASE_DIR, "data", "chat_logs")

os.makedirs(LOGS_DIR, exist_ok=True)

def _log_file(pet_name):
    safe = pet_name.replace(" ", "_").lower()
    return os.path.join(LOGS_DIR, f"{safe}.json")

def save_message(pet_name, sender, text, mood=None):
    path = _log_file(pet_name)
    history = load_history(pet_name)
    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date"     : datetime.now().strftime("%Y-%m-%d"),
        "sender"   : sender,
        "text"     : text,
        "mood"     : mood
    })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_history(pet_name):
    path = _log_file(pet_name)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_today_moods(pet_name):
    history = load_history(pet_name)
    today   = datetime.now().strftime("%Y-%m-%d")
    return [m["mood"] for m in history if m.get("date") == today and m.get("mood")]

def clear_history(pet_name):
    path = _log_file(pet_name)
    if os.path.exists(path):
        os.remove(path)
