import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import pyperclip

# Page configuration
st.set_page_config(page_title="Language Translation Tool", page_icon="🌐", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .title-text {
        text-align: center;
        color: #1f77b4;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        color: gray;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>🌐 Language Translation Tool</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Translate text between multiple languages easily!</p>", unsafe_allow_html=True)
st.write("---")

# Supported languages from deep-translator
@st.cache_data
def get_languages():
    langs = GoogleTranslator().get_supported_languages(as_dict=True)
    # langs is a dict like {'afrikaans': 'af', 'albanian': 'sq', ...}
    return {name.title(): code for name, code in langs.items()}

language_mapping = get_languages()
language_names = list(language_mapping.keys())

# Add Auto Detect option to source
source_languages = ["Auto Detect"] + language_names

if 'source_lang' not in st.session_state:
    st.session_state.source_lang = "Auto Detect"
if 'target_lang' not in st.session_state:
    st.session_state.target_lang = "English"

# Columns for layout
col1, col2, col3 = st.columns([4, 1, 4])

with col1:
    source_lang = st.selectbox("Source Language", source_languages, index=source_languages.index(st.session_state.source_lang), key="src_lang")

with col2:
    st.write("")
    st.write("")
    if st.button("⇄ Swap"):
        if st.session_state.src_lang != "Auto Detect":
            st.session_state.source_lang = st.session_state.tgt_lang
            st.session_state.target_lang = st.session_state.src_lang
            st.rerun()

with col3:
    target_lang = st.selectbox("Target Language", language_names, index=language_names.index(st.session_state.target_lang), key="tgt_lang")

text_col1, text_col2 = st.columns(2)

with text_col1:
    input_text = st.text_area("Enter text to translate:", height=200, placeholder="Type or paste your text here...")

translated_text = ""
detected_lang_name = ""

if input_text:
    try:
        if source_lang == "Auto Detect":
            src_code = "auto"
        else:
            src_code = language_mapping[source_lang]

        tgt_code = language_mapping[target_lang]

        translator = GoogleTranslator(source=src_code, target=tgt_code)
        translated_text = translator.translate(input_text)

        if source_lang == "Auto Detect":
            # Detect the language using deep-translator
            from deep_translator.detection import single_detection
            try:
                detected = single_detection(input_text)
                detected_lang_name = detected.title()
            except Exception:
                detected_lang_name = "Unknown"
            st.info(f"Auto-detected Source Language: **{detected_lang_name}**")

    except Exception as e:
        st.error(f"Error during translation: {e}")

with text_col2:
    st.text_area("Translated text:", value=translated_text, height=200, disabled=True)

# Actions Row
action_col1, action_col2 = st.columns(2)

with action_col1:
    if translated_text:
        if st.button("📋 Copy to Clipboard"):
            try:
                pyperclip.copy(translated_text)
                st.success("Copied to clipboard!")
            except Exception as e:
                # Fallback if pyperclip fails
                st.code(translated_text, language="text")
                st.warning("Clipboard copy might not work in some environments. Use the code block above to copy.")

with action_col2:
    if translated_text:
        if st.button("🔊 Play Translated Text"):
            try:
                tts = gTTS(text=translated_text, lang=language_mapping[target_lang])
                tts.save("temp_audio.mp3")
                st.audio("temp_audio.mp3", format="audio/mp3")
            except Exception as e:
                st.error(f"Text-to-Speech not supported for this language or encountered an error: {e}")

st.markdown("<p class='footer'>Developed with ❤️ using Streamlit & Deep Translator</p>", unsafe_allow_html=True)
