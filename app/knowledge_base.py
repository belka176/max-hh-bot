import requests
from bs4 import BeautifulSoup
from app.database import SessionLocal
from app.models import KnowledgeEntry
import json
import re

HH_DOCS_BASE = "https://github.com/hhru/api/tree/master/docs"

def parse_hh_docs():
    response = requests.get("https://api.hh.ru/openapi/en")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        with open("data/hh_api_docs.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    return []

def seed_knowledge_base():
    db = SessionLocal()
    try:
        docs = parse_hh_docs()
        for item in docs:
            entry = KnowledgeEntry(
                topic=item["topic"],
                question_pattern=item["question"],
                answer=item["answer"],
                source_url=item.get("url", "")
            )
            db.add(entry)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Ошибка загрузки: {e}")
    finally:
        db.close()