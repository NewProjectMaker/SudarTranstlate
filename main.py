from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests

app = FastAPI()

# Ключ будет подтягиваться из настроек Render.com
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

class TextRequest(BaseModel):
    text: str

@app.post("/translate")
def translate_text(req: TextRequest):
    prompt = f"Переведи текст на дореволюционный дворянский русский язык XIX века. Используй обращения 'сударь', 'извольте'. Отвечай СТРОГО только переведенным текстом без пояснений и кавычек: {req.text}"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    body = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=body, headers=headers)
    
    if response.status_code == 200:
        result = response.json()["choices"][0]["message"]["content"]
        return {"result": result.strip()}
    return {"result": req.text}
