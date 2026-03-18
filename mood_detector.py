from translation import MOOD_MAP

MOOD_COLORS = {
    "green" : "#2e7d32",
    "red"   : "#c62828",
    "orange": "#e65100",
    "blue"  : "#1565c0",
    "gray"  : "#555555"
}

def get_mood(sound_key):
    m = MOOD_MAP.get(sound_key, {})
    return {
        "mood" : m.get("mood", "Unknown"),
        "emoji": m.get("emoji", "🐱"),
        "pct"  : m.get("pct", 50),
        "color": m.get("color", "gray")
    }

def get_mood_bar_html(mood, pct, color):
    hex_color = MOOD_COLORS.get(color, "#888888")
    return f"""
    <div style='margin-top:6px'>
      <small style='color:#aaa'>{mood} — {pct}%</small>
      <div style='background:#333;border-radius:8px;height:7px;width:180px;margin-top:3px'>
        <div style='background:{hex_color};width:{pct}%;height:7px;border-radius:8px'></div>
      </div>
    </div>
    """

def summarize_moods(mood_list):
    if not mood_list:
        return {}
    from collections import Counter
    counts = Counter(mood_list)
    total  = len(mood_list)
    return {mood: round(count / total * 100) for mood, count in counts.most_common()}
