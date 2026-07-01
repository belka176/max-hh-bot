import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal, engine
from app.models import KnowledgeEntry
from sqlalchemy import inspect

def check_database():
    """Проверка состояния БД"""
    print("=" * 60)
    print(" ПРОВЕРКА БАЗЫ ДАННЫХ")
    print("=" * 60)
    
    # 1. Проверка подключения
    print("\n Проверка подключения к БД...")
    try:
        with engine.connect() as conn:
            print("    Подключение успешно!")
    except Exception as e:
        print(f"    Ошибка подключения: {e}")
        return
    
    # 2. Проверка таблиц
    print("\n Проверка таблиц...")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if tables:
        print(f"    Найдены таблицы: {', '.join(tables)}")
        for table in tables:
            columns = inspector.get_columns(table)
            print(f"       {table}: {', '.join([col['name'] for col in columns])}")
    else:
        print("    Таблицы не найдены!")
        print("    Создайте таблицы: python db/init_db.py")
        return
    
    # 3. Проверка данных
    print("\n Проверка данных...")
    db = SessionLocal()
    
    try:
        count = db.query(KnowledgeEntry).count()
        print(f"    Всего записей: {count}")
        
        if count > 0:
            print("\n    Примеры записей:")
            for entry in db.query(KnowledgeEntry).limit(5).all():
                print(f"       {entry.question_pattern[:50]}...")
                print(f"      Тема: {entry.topic}")
                print(f"       Источник: {entry.source_url or 'нет'}")
                print()
        else:
            print("    База знаний пуста!")
            print("    Загрузите данные:")
            print("      python db/parser_hh_docs.py   # парсинг документации")
            print("      python db/seed_knowledge_manual.py  # ручные записи")
        
    except Exception as e:
        print(f"    Ошибка при чтении данных: {e}")
    
    finally:
        db.close()
    
    # 4. Статистика
    print("\n" + "=" * 60)
    print(" СТАТИСТИКА")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        # По темам
        topics = db.query(KnowledgeEntry.topic).distinct().all()
        print(f" Количество тем: {len(topics)}")
        
        # По источникам
        sources = db.query(KnowledgeEntry.source_url).distinct().count()
        print(f" Количество источников: {sources}")
        
    except Exception as e:
        print(f" Ошибка статистики: {e}")
    
    finally:
        db.close()
    
    print("\n" + "=" * 60)
    print(" ПРОВЕРКА ЗАВЕРШЕНА")
    print("=" * 60)

if __name__ == "__main__":
    check_database()