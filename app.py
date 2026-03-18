import streamlit as st
from translation import get_cat_translation, get_human_response
from mood_detector import get_mood_bar_html
from tts_helper import text_to_speech
from pet_profile import (add_profile, get_profile, get_all_profile_names,
                          update_mood_history, delete_profile, get_most_common_mood)
from chat_history import save_message, load_history, clear_history
from analytics import show_mood_pie, show_mood_bar_chart

# ─── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="CatTalk 🐱",
    page_icon="🐱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
  .main { background-color: #0f0f0f; }
  .bubble-cat {
    background: linear-gradient(135deg,#1b5e20,#2e7d32);
    color:white; padding:12px 18px;
    border-radius:18px 18px 18px 4px;
    max-width:75%; font-size:15px;
    margin-bottom:4px;
  }
  .bubble-human {
    background: linear-gradient(135deg,#0d47a1,#1a73e8);
    color:white; padding:12px 18px;
    border-radius:18px 18px 4px 18px;
    max-width:75%; font-size:15px;
    margin-left:auto; margin-bottom:4px;
  }
  .stButton>button {
    border-radius:20px; padding:6px 18px; font-weight:600;
  }
  .cat-btn>button {
    background:#1b5e20; color:white; border:none;
    width:100%; margin-bottom:6px;
  }
</style>
""", unsafe_allow_html=True)

# ─── Session State ─────────────────────────────────────────
if "messages"    not in st.session_state: st.session_state.messages    = []
if "active_pet"  not in st.session_state: st.session_state.active_pet  = None
if "show_analytics" not in st.session_state: st.session_state.show_analytics = False

# ─── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🐱 CatTalk")
    st.markdown("---")

    # Language toggle
    lang = st.radio("🔊 TTS Language", ["English", "Hindi"], horizontal=True)
    lang_code = "en" if lang == "English" else "hi"
    st.markdown("---")

    # Pet Profile section
    st.markdown("### 🐾 Pet Profile")
    pet_names = get_all_profile_names()

    if pet_names:
        selected = st.selectbox("Select your pet", pet_names)
        st.session_state.active_pet = selected
        profile = get_profile(selected)
        if profile:
            st.markdown(f"""
            **Name:** {profile['name']}
            **Breed:** {profile['breed']}
            **Age:** {profile['age']} years
            **Most common mood:** {get_most_common_mood(selected)}
            **Total chats:** {profile['total_chats']}
            """)
            if st.button("🗑️ Delete Profile"):
                delete_profile(selected)
                st.rerun()

    st.markdown("#### Add New Pet")
    with st.expander("➕ New profile"):
        p_name  = st.text_input("Cat's name")
        p_breed = st.text_input("Breed (e.g. Persian)")
        p_age   = st.number_input("Age (years)", min_value=0, max_value=30, value=1)
        p_about = st.text_area("About your cat", placeholder="Lazy but loveable...")
        if st.button("Save Profile"):
            if p_name.strip():
                add_profile(p_name.strip(), p_breed, p_age, p_about)
                st.success(f"{p_name} added!")
                st.rerun()

    st.markdown("---")
    if st.button("📊 Show Analytics"):
        st.session_state.show_analytics = not st.session_state.show_analytics

# ─── MAIN AREA ─────────────────────────────────────────────
st.markdown("## 🐱 CatTalk — Animal Human Translator")

if not st.session_state.active_pet:
    st.warning("👈 Pehle sidebar mein apni cat ka profile banao!")
    st.stop()

active_pet = st.session_state.active_pet
st.markdown(f"**Chatting with:** 🐱 {active_pet}")
st.markdown("---")

# ─── ANALYTICS ─────────────────────────────────────────────
if st.session_state.show_analytics:
    st.markdown("### 📊 Mood Analytics")
    col_a, col_b = st.columns(2)
    with col_a:
        show_mood_pie(active_pet)
    with col_b:
        show_mood_bar_chart(active_pet)
    st.markdown("---")

# ─── CHAT INPUT AREA ───────────────────────────────────────
col_cat, col_human = st.columns(2)

# CAT SIDE
with col_cat:
    st.markdown("### 🐱 Cat Side")
    st.markdown("Cat ne kya bola? Select karo:")

    CAT_BUTTONS = [
        ("😺 Short Meow",      "meow"),
        ("😿 Multiple Meows",  "multiple_meow"),
        ("😾 Long Meow",       "long_meow"),
        ("😻 Purring",         "purr"),
        ("🙀 Hissing",         "hiss"),
        ("😤 Growling",        "growl"),
        ("😹 Chirping",        "chirp"),
        ("🥰 Trilling",        "trill"),
        ("😱 Yowling",         "yowl"),
        ("😶 Silent Meow",     "silent_meow"),
        ("😠 Chattering",      "chatter"),
    ]

    for label, key in CAT_BUTTONS:
        if st.button(label, key=f"cat_{key}", use_container_width=True):
            data = get_cat_translation(key, lang_code)
            msg = {
                "sender" : "cat",
                "sound"  : label,
                "text"   : data["text"],
                "mood"   : data["mood"],
                "emoji"  : data["emoji"],
                "pct"    : data["pct"],
                "color"  : data["color"],
                "lang"   : lang_code
            }
            st.session_state.messages.append(msg)
            save_message(active_pet, "cat", data["text"], data["mood"])
            update_mood_history(active_pet, data["mood"])

# HUMAN SIDE
with col_human:
    st.markdown("### 🧑 Human Side")
    user_input = st.text_input(
        "Tum kya bolna chahte ho?",
        placeholder="Kuch bhi likho...",
        key="human_input"
    )
    if st.button("📤 Send", use_container_width=True):
        if user_input.strip():
            response = get_human_response(user_input)
            msg = {
                "sender"  : "human",
                "text"    : user_input,
                "response": response,
                "lang"    : lang_code
            }
            st.session_state.messages.append(msg)
            save_message(active_pet, "human", user_input)

# ─── CHAT DISPLAY ──────────────────────────────────────────
st.markdown("---")
st.markdown("### 💬 Conversation")

if not st.session_state.messages:
    st.info("Abhi koi conversation nahi! Upar se shuru karo 🐾")
else:
    for i, msg in enumerate(reversed(st.session_state.messages)):
        if msg["sender"] == "cat":
            mood_bar = get_mood_bar_html(msg["mood"], msg["pct"], msg["color"])
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"""
                <div class='bubble-cat'>
                  {msg['emoji']} <b>Cat said:</b> {msg['sound']}<br>
                  💬 <i>"{msg['text']}"</i>
                  {mood_bar}
                </div>
                """, unsafe_allow_html=True)
            with c2:
                if st.button("🔊", key=f"tts_cat_{i}", help="Listen"):
                    audio = text_to_speech(msg["text"], msg["lang"])
                    if audio:
                        st.audio(audio)

        elif msg["sender"] == "human":
            c1, c2 = st.columns([1, 5])
            with c2:
                st.markdown(f"""
                <div class='bubble-human'>
                  🧑 <b>You said:</b> "{msg['text']}"<br>
                  🐱 <b>Cat thinks:</b> {msg['response']}
                </div>
                """, unsafe_allow_html=True)
            with c1:
                if st.button("🔊", key=f"tts_human_{i}", help="Listen"):
                    audio = text_to_speech(msg["response"], msg["lang"])
                    if audio:
                        st.audio(audio)

# ─── CLEAR ─────────────────────────────────────────────────
st.markdown("---")
col_clr1, col_clr2 = st.columns(2)
with col_clr1:
    if st.button("🗑️ Clear Chat (screen only)"):
        st.session_state.messages = []
        st.rerun()
with col_clr2:
    if st.button("🗑️ Clear Full History"):
        clear_history(active_pet)
        st.session_state.messages = []
        st.rerun()
