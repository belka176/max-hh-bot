import uvicorn
from app.yandex_assistant import app

if __name__ == "__main__":
    uvicorn.run("app.yandex_assistant:app", host="0.0.0.0", port=8000, reload=True)