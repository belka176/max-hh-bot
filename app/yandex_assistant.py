from fastapi import FastAPI, Request
from app.response_generator import ResponseGenerator
import httpx 

app = FastAPI()
rg = ResponseGenerator()
BOT_TOKEN = "ваш_токен_из_шага_2" 

@app.post("/") 
async def max_webhook(request: Request):
    data = await request.json()
    user_text = data.get("message", {}).get("text", "")
 
    answer = rg.generate(user_text)
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://api.max.ru/bot/v1/sendMessage", 
            json={"chat_id": data["message"]["chat"]["id"], "text": answer},
            headers={"Authorization": f"Bearer {BOT_TOKEN}"}
        )
    return {"status": "ok"}