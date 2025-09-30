# Realtime Voice Chatbot

A real-time voice-based chatbot powered by **Whisper** for speech-to-text, **Groq LLM (LLaMA 3)** for conversational AI, and **gTTS** for text-to-speech. Users can talk naturally and get fun, short, and witty replies from Clara.

---

## Features

- Real-time voice interaction via browser.
- Speech-to-text using OpenAI's Whisper model.
- Conversational AI powered by Groq LLaMA 3.
- Text-to-speech with Google Text-to-Speech (gTTS).
- Conversation history support (last 10 messages).
- Friendly, concise, and casual AI personality.
- Audio playback of bot responses in browser.


---

## Tech Stack

- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, JavaScript
- **Models:** Whisper, Groq LLaMA 3, gTTS

---

## How to Run

1. **Clone the repository and install dependencies**

```bash
git clone <url>
cd realtime_voice_chatbot
```
```
pip install -r requirements.txt
```


2. **Add Your Groq API Key**

Edit the `.env` file in the root directory and replace it with your key:

```
GROQ_API_KEY = your_groq_api_key
```

You can get the GROQ API KEY from [here](https://console.groq.com/keys)


3. **Start backend server**
   
Open terminal and enter:

```
python main.py
```
The server will run at http://localhost:8000

4. **Launch frontend**
   
Open index.html in your browser
