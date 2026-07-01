from app.intent_parser import IntentParser
from app.database import SessionLocal
from app.models import KnowledgeEntry

class ResponseGenerator:
    def __init__(self):
        self.parser = None
        self._load_data()
    
    def _load_data(self):
        try:
            db = SessionLocal()
            entries = db.query(KnowledgeEntry).all()
            db.close()
            
            if entries:
                questions = [e.question_pattern for e in entries]
                answers = [e.answer for e in entries]
                self.parser = IntentParser(questions, answers)
                print(f" Загружено {len(entries)} записей из БД")
            else:
                print(" База знаний пуста. Сначала загрузите данные.")
        except Exception as e:
            print(f" Не удалось загрузить данные из БД: {e}")
            print("   Возможно, таблицы еще не созданы. Запустите db/init_db.py")
    
    def generate(self, user_query):
        if not self.parser:
            return "База знаний еще не загружена. Попробуйте позже или запустите db/init_db.py"
        
        answer = self.parser.get_best_answer(user_query)
        if answer:
            return answer
        return "Извините, я не нашел ответ на ваш вопрос."