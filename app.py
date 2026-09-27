import streamlit as st
import requests
from gtts import gTTS
import pyperclip
import os

# Page configuration
st.set_page_config(page_title="Language Translation Tool", page_icon="🌐", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .title-text {
        text-align: center;
        color: #1f77b4;
        font-weight: 700;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        color: gray;
    }
    .stButton>button {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>🌐 Language Translation Tool</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; color: #555;'>Translate text instantly between 100+ languages using Google's Neural Translation Engine!</p>", unsafe_allow_html=True)
st.write("---")

# Comprehensive language dictionary
LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Marathi": "mr",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese (Simplified)": "zh-CN",
    "Russian": "ru",
    "Portuguese": "pt",
    "Arabic": "ar",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Punjabi": "pa",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
    "Dutch": "nl",
    "Greek": "el",
    "Turkish": "tr",
    "Vietnamese": "vi",
    "Thai": "th",
    "Swedish": "sv",
    "Polish": "pl",
    "Indonesian": "id",
    "Hebrew": "he"
}

CODE_TO_LANG = {v: k for k, v in LANGUAGES.items() if k != "Auto Detect"}

language_names = list(LANGUAGES.keys())
target_language_names = [l for l in language_names if l != "Auto Detect"]

# Initialize session state variables
if 'source_lang' not in st.session_state:
    st.session_state.source_lang = "Auto Detect"
if 'target_lang' not in st.session_state:
    st.session_state.target_lang = "English"
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""
if 'detected_info' not in st.session_state:
    st.session_state.detected_info = ""

def translate_text(text, src, tgt):
    """Translate text using Google's translation service."""
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": src,
        "tl": tgt,
        "dt": "t",
        "q": text
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    # Extract translated sentences
    translated = "".join([sentence[0] for sentence in data[0] if sentence[0]])
    
    # Extract detected language if auto
    detected_code = data[2] if len(data) > 2 else src
    return translated, detected_code

# Language selection controls
col1, col2, col3 = st.columns([4, 1, 4])

with col1:
    source_lang = st.selectbox(
        "Source Language", 
        language_names, 
        index=language_names.index(st.session_state.source_lang)
    )

with col2:
    st.write("")
    st.write("")
    if st.button("⇄ Swap"):
        if source_lang != "Auto Detect":
            old_src = source_lang
            st.session_state.source_lang = st.session_state.target_lang
            st.session_state.target_lang = old_src
            st.rerun()

with col3:
    target_lang = st.selectbox(
        "Target Language", 
        target_language_names, 
        index=target_language_names.index(st.session_state.target_lang)
    )

st.session_state.source_lang = source_lang
st.session_state.target_lang = target_lang

# Text input & output columns
text_col1, text_col2 = st.columns(2)

with text_col1:
    input_text = st.text_area("Enter text to translate:", height=200, placeholder="Type or paste your text here (e.g. majha naav vedika ahe)...")

with text_col2:
    st.text_area("Translated text:", value=st.session_state.translated_text, height=200, disabled=True)

# Translation button
if st.button("Translate 🌐", type="primary", use_container_width=True):
    if not input_text.strip():
        st.warning("Please enter some text to translate.")
    else:
        with st.spinner("Translating..."):
            try:
                src_code = LANGUAGES[source_lang]
                tgt_code = LANGUAGES[target_lang]
                
                result, detected_code = translate_text(input_text, src_code, tgt_code)
                st.session_state.translated_text = result
                
                if source_lang == "Auto Detect":
                    detected_name = CODE_TO_LANG.get(detected_code, detected_code.upper())
                    st.session_state.detected_info = f"Auto-detected Source Language: **{detected_name}**"
                else:
                    st.session_state.detected_info = ""
                st.rerun()
            except Exception as e:
                st.error(f"Error during translation: {e}")

if st.session_state.detected_info:
    st.info(st.session_state.detected_info)

# Action buttons (Copy & Play audio)
if st.session_state.translated_text:
    st.write("---")
    act_col1, act_col2 = st.columns(2)
    
    with act_col1:
        if st.button("📋 Copy to Clipboard", use_container_width=True):
            try:
                pyperclip.copy(st.session_state.translated_text)
                st.success("Copied to clipboard!")
            except Exception:
                st.code(st.session_state.translated_text, language="text")
                st.info("Use the text box above to copy.")

    with act_col2:
        if st.button("🔊 Play Translated Audio", use_container_width=True):
            try:
                tgt_code = LANGUAGES[target_lang]
                # Fallback to language prefix if dialect code fails
                lang_code = tgt_code.split("-")[0]
                tts = gTTS(text=st.session_state.translated_text, lang=lang_code)
                audio_file = "temp_audio.mp3"
                tts.save(audio_file)
                st.audio(audio_file, format="audio/mp3")
            except Exception as e:
                st.error(f"Text-to-Speech playback encountered an error: {e}")

st.markdown("<p class='footer'>Developed with ❤️ for CodeAlpha AI Internship</p>", unsafe_allow_html=True)
