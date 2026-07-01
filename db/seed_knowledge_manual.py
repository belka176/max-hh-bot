#!/usr/bin/env python
"""
Ручное наполнение базы знаний типовыми вопросами
Запуск: python db/seed_knowledge_manual.py
"""

import os
import sys

# Добавляем путь к корню проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import KnowledgeEntry

# Типовые вопросы и ответы по API HH.ru
MANUAL_ENTRIES = [
    {
        "topic": "Авторизация",
        "question": "Как получить access-токен для API HH.ru?",
        "answer": """Для получения access-токена используйте OAuth 2.0.
        
Шаги:
1. Зарегистрируйте приложение на https://dev.hh.ru
2. Получите client_id и client_secret
3. Используйте авторизацию пользователя или приложения
4. Получите access_token и refresh_token

Подробнее: https://api.hh.ru/openapi/redoc#section/Avtorizaciya""",
        "source": "authorization.md"
    },
    {
        "topic": "Вакансии",
        "question": "Как получить список вакансий?",
        "answer": """Используйте GET запрос к /vacancies.

Основные параметры:
- text — текст поиска
- area — регион (id)
- salary — зарплата
- employment — тип занятости
- experience — опыт работы
- per_page — количество на странице (до 100)
- page — номер страницы

Пример: GET /vacancies?text=Python&area=1&per_page=20""",
        "source": "vacancies.md"
    },
    {
        "topic": "Отклики",
        "question": "Как откликнуться на вакансию через API?",
        "answer": """Используйте POST запрос к /negotiations.

Обязательные параметры:
- vacancy_id — ID вакансии
- resume_id — ID резюме

Опционально:
- message — сопроводительное письмо

Пример: POST /negotiations?vacancy_id=123456&resume_id=789012""",
        "source": "negotiations.md"
    },
    {
        "topic": "Резюме",
        "question": "Как получить резюме соискателя?",
        "answer": """Используйте GET запрос к /resumes/{resume_id}.

Важно:
- Для работодателей требуется платный доступ к базе резюме
- Возвращает полную информацию о резюме
- Контакты видны только при оплаченном доступе

Пример: GET /resumes/0123456789abcdef""",
        "source": "employer_resumes.md"
    },
    {
        "topic": "Ошибки",
        "question": "Что означает ошибка 403 при запросе к API?",
        "answer": """Ошибка 403 (Forbidden) означает, что у вас нет прав на выполнение запроса.

Возможные причины:
1. Отсутствует или невалидный access_token
2. Недостаточно прав у пользователя
3. Превышен лимит запросов
4. Нет оплаченного доступа к методу

Решение:
- Проверьте авторизацию
- Обновите токен
- Проверьте права доступа""",
        "source": "errors.md"
    },
    {
        "topic": "Поиск",
        "question": "Как искать вакансии с фильтрацией?",
        "answer": """Используйте GET /vacancies с параметрами фильтрации.

Популярные фильтры:
- employment — полная, частичная, проектная и др.
- experience — noExperience, between1And3, between3And6, moreThan6
- schedule — удаленная работа, гибкий график
- only_with_salary — только с указанной зарплатой
- date_from — дата публикации от

Пример: 
GET /vacancies?text=Python&experience=between1And3&employment=full""",
        "source": "vacancies_for_applicant.md"
    },
    {
        "topic": "Справочники",
        "question": "Где взять справочники регионов и метро?",
        "answer": """Справочники доступны через API:
- Регионы: GET /areas
- Метро: GET /metro
- Специализации: GET /specializations
- Ключевые навыки: GET /skill_set

Данные кэшируются, обновляйте при необходимости.
Используйте Etag для оптимизации.""",
        "source": "areas.md"
    }
]

def seed_manual_entries():
    """Добавление вручную подготовленных вопросов-ответов"""
    print("=" * 60)
    print(" Ручное наполнение базы знаний")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Проверяем, есть ли уже такие записи
        existing_count = 0
        new_count = 0
        
        for entry_data in MANUAL_ENTRIES:
            # Проверяем, есть ли уже такой вопрос
            existing = db.query(KnowledgeEntry).filter(
                KnowledgeEntry.question_pattern == entry_data["question"]
            ).first()
            
            if existing:
                existing_count += 1
                print(f"  Уже есть: {entry_data['question'][:40]}...")
            else:
                entry = KnowledgeEntry(**entry_data)
                db.add(entry)
                new_count += 1
                print(f" Добавлен: {entry_data['question'][:40]}...")
        
        db.commit()
        db.close()
        
        print("\n" + "=" * 60)
        print(f" Результат:")
        print(f"   Добавлено новых: {new_count}")
        print(f"   Уже существовало: {existing_count}")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        db.close()
        print(f" Ошибка при сохранении: {e}")

def show_sample():
    """Показать примеры записей в БД"""
    db = SessionLocal()
    entries = db.query(KnowledgeEntry).limit(5).all()
    
    if entries:
        print("\n📋 Примеры записей в базе знаний:")
        for entry in entries:
            print(f"   {entry.question_pattern[:60]}...")
            print(f"   {entry.topic}")
            print()
    
    db.close()

if __name__ == "__main__":
    seed_manual_entries()
    show_sample()