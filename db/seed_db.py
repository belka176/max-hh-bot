import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import KnowledgeEntry

def seed_database():
    """Загрузка данных"""
    print(" Загрузка базы знаний...")
    
    db = SessionLocal()
    
    # Проверяем, есть ли данные
    count = db.query(KnowledgeEntry).count()
    if count > 0:
        print(f" В БД уже есть {count} записей")
        response = input("Удалить старые и загрузить новые? (y/n): ")
        if response.lower() != 'y':
            db.close()
            return
        db.query(KnowledgeEntry).delete()
        db.commit()
    
    # Данные для загрузки
    data = [
        {
            "topic": "Вакансии",
            "question_pattern": "Как получить список вакансий?",
            "answer": "Используйте GET запрос к /vacancies",
            "source_url": "https://api.hh.ru/openapi/"
        },
        {
            "topic": "Авторизация",
            "question_pattern": "Как получить токен?",
            "answer": "Используйте OAuth 2.0 на https://oauth.hh.ru/",
            "source_url": "https://api.hh.ru/openapi/"
        },
        {
            "topic": "Резюме",
            "question_pattern": "Как создать резюме?",
            "answer": "Используйте POST запрос к /resumes",
            "source_url": "https://api.hh.ru/openapi/"
        }
    ]
    
    for item in data:
        entry = KnowledgeEntry(**item)
        db.add(entry)
    
    db.commit()
    db.close()
    print(f" Загружено {len(data)} записей!")

if __name__ == "__main__":
    seed_database()