MAX — Чат-бот для HH.ru API на Yandex Assistant
Описание
Чат-бот для разработчиков API HeadHunter, интегрированный с Yandex Assistant (Алиса). Помогает находить ответы на вопросы по документации, снижает нагрузку на поддержку.

Это проект по практике.

Технологии
FastAPI

SQLAlchemy + PostgreSQL

Yandex Assistant (навык)

Scikit-learn (TF-IDF + косинусная близость)

 Запуск сервера
Откройте терминал Ubuntu и выполните:
```
cd ~/max-hh-bot
source venv/bin/activate
uvicorn app.yandex_assistant:app --host 0.0.0.0 --port 8000 --reload
```
Проверка работы бота
Откройте новое окно терминала Ubuntu и выполните:
```
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '{"request": {"command": "Как получить access-токен?"}, "session": {}, "version": "1.0"}'
  ```