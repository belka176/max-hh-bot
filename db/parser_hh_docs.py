import os
import re
import json
from pathlib import Path

def parse_md_files(docs_folder="docs"):
    """Парсинг всех .md файлов из папки docs"""
    questions_answers = []
    
    # Проходим по всем .md файлам
    for md_file in Path(docs_folder).glob("*.md"):
        print(f" Обработка: {md_file.name}")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Извлекаем заголовки (вопросы)
        headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        
        # Извлекаем примеры запросов и ответов
        endpoints = re.findall(r'`(GET|POST|PUT|DELETE)\s+([^`]+)`', content)
        
        # Извлекаем описание полей
        fields = re.findall(r'\|\s*([a-zA-Z_]+)\s*\|\s*([^\|]+)\s*\|', content)
        
        # Формируем вопросы-ответы
        for header in headers:
            if any(keyword in header.lower() for keyword in ['как', 'что', 'где', 'когда', 'почему']):
                question = header
                # Ищем описание под заголовком
                pattern = rf'#+\s+{re.escape(header)}.*?\n(.*?)(?=\n#+|\Z)'
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    answer = match.group(1).strip()
                    questions_answers.append({
                        "topic": md_file.stem.replace('_', ' ').title(),
                        "question": question,
                        "answer": answer[:500] + "..." if len(answer) > 500 else answer,
                        "source": md_file.name
                    })
        
        # Добавляем эндпоинты как вопросы
        for method, endpoint in endpoints:
            questions_answers.append({
                "topic": md_file.stem.replace('_', ' ').title(),
                "question": f"Как использовать {method} {endpoint}?",
                "answer": f"Эндпоинт: {method} {endpoint}\nДокументация: {md_file.name}",
                "source": md_file.name
            })
    
    return questions_answers

def save_to_db(data):
    """Сохранение данных в базу знаний"""
    from app.database import SessionLocal
    from app.models import KnowledgeEntry
    
    db = SessionLocal()
    
    # Очищаем старые данные
    db.query(KnowledgeEntry).delete()
    db.commit()
    
    # Загружаем новые
    for item in data:
        entry = KnowledgeEntry(
            topic=item["topic"],
            question_pattern=item["question"],
            answer=item["answer"],
            source_url=f"https://github.com/hhru/api/blob/master/docs/{item['source']}"
        )
        db.add(entry)
    
    db.commit()
    db.close()
    print(f" Загружено {len(data)} записей")

if __name__ == "__main__":
    print(" Начинаем парсинг документации HH.ru...")
    
    # Создаем папку docs, если её нет
    os.makedirs("docs", exist_ok=True)
    
    # Парсим
    data = parse_md_files()
    
    # Сохраняем JSON (для отладки)
    with open("data/hh_api_docs.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Сохраняем в БД
    save_to_db(data)
    
    print(" Готово! База знаний наполнена.")