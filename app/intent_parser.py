import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class IntentParser:
    def __init__(self, questions, answers):
        self.vectorizer = TfidfVectorizer()
        self.questions = questions
        self.answers = answers
        self.vectors = self.vectorizer.fit_transform(questions)
    
    def get_best_answer(self, query):
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.vectors)
        best_idx = np.argmax(similarities)
        if similarities[0][best_idx] < 0.1:  
            return None
        return self.answers[best_idx]