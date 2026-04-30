from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import edge_tts
import asyncio
import io

app = FastAPI()

VOICE = "vi-VN-HoaiMyNeural"

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/tts")
async def tts(text: str):
    try:
        communicate = edge_tts.Communicate(text, VOICE)

        audio_bytes = b""

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_bytes += chunk["data"]

        return StreamingResponse(
            io.BytesIO(audio_bytes),
            media_type="audio/mpeg"
        )

    except Exception as e:
        print("ERROR:", str(e))  # 🔥 LOG RA CONSOLE
        return {"error": str(e)}