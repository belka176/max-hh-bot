import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base
from app.models import KnowledgeEntry

def create_tables():
    """Создание всех таблиц"""
    print(" Создание таблиц в базе данных...")
    
    try:
        # Создаем таблицы
        Base.metadata.create_all(bind=engine)
        print(" Таблицы успешно созданы!")
        
        # Проверяем, какие таблицы создались
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if tables:
            print(f" Созданы таблицы: {', '.join(tables)}")
            for table in tables:
                columns = inspector.get_columns(table)
                print(f"   {table}: {', '.join([col['name'] for col in columns])}")
        else:
            print(" Таблицы не найдены. Проверьте модели.")
            
    except Exception as e:
        print(f" Ошибка: {e}")
        print("\nПроверьте подключение к БД и настройки в .env")

if __name__ == "__main__":
    create_tables()