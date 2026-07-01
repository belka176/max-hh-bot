import sys
import os

# Добавляем путь к корню проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем только нужные компоненты
from app.database import engine, Base

def init_database():
    """Создание всех таблиц"""
    print(" Создание таблиц в базе данных...")
    
    try:
        # Создаем таблицы
        Base.metadata.create_all(bind=engine)
        print(" Таблицы успешно созданы!")
        
        # Проверяем
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if tables:
            print(f" Созданы таблицы: {', '.join(tables)}")
        else:
            print(" Таблицы не найдены.")
            
    except Exception as e:
        print(f" Ошибка: {e}")

if __name__ == "__main__":
    init_database()