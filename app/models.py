from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base

class KnowledgeEntry(Base):
    __tablename__ = "knowledge_entries"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(200), nullable=False)
    question_pattern = Column(String(300), nullable=False)
    answer = Column(Text, nullable=False)
    source_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)