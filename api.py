from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import edge_tts
import hashlib
from cachetools import LRUCache
import io

app = FastAPI()

tts_cache = LRUCache(maxsize=500)

VOICE = "vi-VN-HoaiMyNeural"

def make_key(text):
    return hashlib.md5(text.encode()).hexdigest()

async def generate_tts(text):
    communicate = edge_tts.Communicate(
        text,
        VOICE,
        rate="+5%",
        pitch="+2Hz"
    )
    audio = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio += chunk["data"]
    return audio

@app.get("/tts")
async def tts(text: str):
    key = make_key(text)

    if key in tts_cache:
        return StreamingResponse(io.BytesIO(tts_cache[key]), media_type="audio/mpeg")

    audio = await generate_tts(text)
    tts_cache[key] = audio

    return StreamingResponse(io.BytesIO(audio), media_type="audio/mpeg")