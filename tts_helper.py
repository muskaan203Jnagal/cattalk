from gtts import gTTS
import tempfile
import os

def text_to_speech(text, lang="en"):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp.name)
        return tmp.name
    except Exception as e:
        print(f"TTS error: {e}")
        return None

def cleanup_audio(filepath):
    try:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
    except:
        pass
