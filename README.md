# Language Translation Tool

A modern, complete Language Translation web application built using Python, Streamlit, Googletrans, and gTTS (Google Text-to-Speech).

## Features

- **Multi-language Support:** Translate text between 100+ languages.
- **Auto-Detection:** Automatically detect the source language of the input text.
- **Language Swapping:** Easily swap source and target languages with a click.
- **Text-to-Speech (TTS):** Listen to the translated text using Google TTS.
- **Copy to Clipboard:** Copy the translated text quickly.
- **Modern UI:** Clean, responsive, and easy-to-use interface powered by Streamlit.

## Screenshots

*(Add screenshots of your application here)*

## Technologies Used

- **Python**
- **Streamlit:** For creating the interactive web interface.
- **googletrans==4.0.0rc1:** For fetching translations (Free API).
- **gTTS:** For Text-to-Speech functionality.
- **pyperclip:** For clipboard integration.

## Installation

1. Clone this repository or download the source code.
2. Ensure you have Python 3.7+ installed.
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:

```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (usually `http://localhost:8501`).
3. Enter the text you wish to translate in the left box.
4. Select the source language (or use "Auto Detect") and the target language.
5. The translation will automatically appear in the right box.
6. Use the **Copy to Clipboard** button to copy the translation or **Play Translated Text** to listen to it.

## License

This project is open-source and available under the MIT License.
