from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.response_generator import ResponseGenerator

app = FastAPI()

# Инициализируем генератор
rg = ResponseGenerator()

class AliceRequest(BaseModel):
    request: dict
    session: dict
    version: str

@app.post("/")
async def alice_webhook(req: AliceRequest):
    user_text = req.request.get("command", "")
    answer = rg.generate(user_text)
    
    return {
        "response": {
            "text": answer,
            "end_session": False
        },
        "session": req.session,
        "version": req.version
    }

@app.get("/")
async def root():
    return {"message": "MAX Bot is running!"}