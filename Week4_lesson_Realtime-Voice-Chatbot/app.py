from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import whisper
import groq
from gtts import gTTS
from collections import deque
import base64
import tempfile
import os
import io
import traceback
from dotenv import load_dotenv
import uvicorn

load_dotenv()

# Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a casual, short, and conversational AI assistant, and your name is Clara."
        "Keep replies friendly, natural and concise unless asked for more detail."
        "Be fun and witty in your replies where possible."
    )
}

app = FastAPI(title="Realtime Voice Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


whisper_model = whisper.load_model("base")
groq_client = groq.Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
conversation_history = deque(maxlen=10)


@app.get("/")
async def root():
    return {"message": "Chatbot running"}


@app.post("/chat")
async def chat(audio_file: UploadFile = File(...)):
    temp_path = None
    try:
        content_type = (audio_file.content_type or "").lower()
        original_name = (audio_file.filename or "").lower()

        if "webm" in content_type or original_name.endswith(".webm"):
            suffix = ".webm"
        elif "ogg" in content_type or original_name.endswith(".ogg"):
            suffix = ".ogg"
        elif "mp3" in content_type or original_name.endswith(".mp3") or "mpeg" in content_type:
            suffix = ".mp3"
        else:
            suffix = ".wav"

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tf:
            content = await audio_file.read()
            tf.write(content)
            temp_path = tf.name

        # Transcribe with Whisper (Speech to Text)
        transcription = whisper_model.transcribe(temp_path)
        user_text = transcription.get("text", "").strip()

        if not user_text:
            response_text = "I didn't get that — could you try again?"
        else:
            if not groq_client:
                raise HTTPException(status_code=500, detail="Groq API key not configured on server.")

            messages = [SYSTEM_PROMPT] + list(conversation_history) + [{"role": "user", "content": user_text}]

            # Ask LLM
            chat_completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                max_tokens=150,
                temperature=0.6,
            )
            response_text = chat_completion.choices[0].message.content.strip()

            # Update conversation history
            conversation_history.append({"role": "user", "content": user_text})
            conversation_history.append({"role": "assistant", "content": response_text})

        # Convert bot reply to speech (gTTS)
        tts_buffer = io.BytesIO()
        tts = gTTS(text=response_text, lang="en", slow=False)
        tts.write_to_fp(tts_buffer)
        tts_buffer.seek(0)
        audio_bytes = tts_buffer.read()
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        return JSONResponse(
            {
                "user_transcription": user_text,
                "bot_response": response_text,
                "audio_base64": audio_b64,
                "audio_mime": "audio/mpeg",
            }
        )

    except Exception as e:
        tb = traceback.format_exc()
        # cleanup
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"{str(e)}\n\n{tb}")

    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except:
                pass


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
