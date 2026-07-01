from app.intent_parser import IntentParser
from app.database import SessionLocal
from app.models import KnowledgeEntry

class ResponseGenerator:
    def __init__(self):
        self.parser = None
        self._load_data()
    
    def _load_data(self):
        db = SessionLocal()
        entries = db.query(KnowledgeEntry).all()
        questions = [e.question_pattern for e in entries]
        answers = [e.answer for e in entries]
        db.close()
        if questions:
            self.parser = IntentParser(questions, answers)
    
    def generate(self, user_query):
        if not self.parser:
            return "База знаний еще не загружена. Попробуйте позже."
        answer = self.parser.get_best_answer(user_query)
        if answer:
            return answer
        return "Извините, я не нашел ответ на ваш вопрос. Возможно, вы имели в виду что-то другое?"