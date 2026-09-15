import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class TranslateRequest(BaseModel):
    text: str

@app.post("/translate")
async def translate(req: TranslateRequest):
    if not req.text.strip():
        return {"result": ""}

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Ты — дворянин XIX века. Перепиши данный текст в изысканном дворянском стиле того времени, сохраняя исходный смысл. Возвращай ТОЛЬКО переведенный текст без кавычек и лишних пояснений."
                },
                {"role": "user", "content": req.text}
            ],
            temperature=0.7
        )
        translated_text = response.choices[0].message.content.strip()
        return {"result": translated_text}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": "Ошибка при обработке запроса"}, 500
