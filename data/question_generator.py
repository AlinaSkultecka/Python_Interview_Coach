import json
import random
import os

from models.flashcards_questions import OpenQuestion
from models.quiz_question import QuizQuestion

# File paths
FLASHCARDS_FILE = os.path.join("data", "quiz_flashcards", "flashcards.json")
QUIZ_QUESTIONS_FILE = os.path.join("data", "quiz_flashcards", "quiz_questions.json")

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_flashcard(topic=None):
    flashcards = load_json(FLASHCARDS_FILE)
    if topic:
        flashcards = [fc for fc in flashcards if fc.get("topic") == topic]
        if not flashcards:
            raise ValueError(f"No flashcards found for topic: {topic}")
    return OpenQuestion.from_dict(random.choice(flashcards))

def generate_quiz_question(topic=None) -> QuizQuestion:
    quiz_questions = load_json(QUIZ_QUESTIONS_FILE)
    if topic:
        quiz_questions = [q for q in quiz_questions if q.get("topic") == topic]
        if not quiz_questions:
            raise ValueError(f"No quiz questions found for topic: {topic}")
    q_dict = random.choice(quiz_questions)
    return QuizQuestion.from_dict(q_dict)

# Alias for compatibility with other parts of your app
generate_open_question = generate_flashcard


# Example usage (you can remove this in production)
if __name__ == "__main__":
    print("Flashcard:", generate_flashcard())
    print("Quiz question:", generate_quiz_question())
    print("Open question:", generate_open_question())