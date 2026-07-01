"""
Пакет приложения MAX чат-бот
"""
__version__ = "1.0.0"

from .config import Config
from .database import SessionLocal, engine, Base
from .models import KnowledgeEntry
from .response_generator import ResponseGenerator
from .yandex_assistant import app
print(f"MAX Bot v{__version__} загружен!")

__all__ = [
    "Config",
    "SessionLocal", 
    "engine",
    "Base",
    "KnowledgeEntry",
    "ResponseGenerator",
    "app"
]