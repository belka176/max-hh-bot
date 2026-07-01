# MAX — Чат-бот для HH.ru API на Yandex Assistant

## Описание
Чат-бот для разработчиков API HeadHunter, интегрированный с Yandex Assistant (Алиса). Помогает находить ответы на вопросы по документации, снижает нагрузку на поддержку. ЭТО ПРОЕКТ ПО ПРАКТИКЕ.

## Технологии
- FastAPI
- SQLAlchemy + PostgreSQL
- Yandex Assistant (навык)
- Scikit-learn (TF-IDF + косинусная близость)

## Установка
1. Клонируйте репозиторий
2. Создайте виртуальное окружение: `python -m venv venv`
3. Активируйте: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
4. Установите зависимости: `pip install -r requirements.txt`
5. Создайте `.env` из `.env.example`
6. Настройте PostgreSQL и создайте БД
7. Запустите: `python -m app.main`

## Описание .env
| Поле | Описание | Пример |
|------|----------|--------|
| DB_HOST | Хост БД | localhost |
| DB_PORT | Порт БД | 5432 |
| DB_USER | Пользователь | postgres |
| DB_PASSWORD | Пароль | 123456 |
| DB_NAME | Имя БД | hh_bot_db |
| YA_ALICE_TOKEN | Токен Яндекса | `y0_...` |
| SKILL_ID | ID навыка | `abcd-...` |

