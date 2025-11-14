import json
import random
import os

from models.flashcards_questions import OpenQuestion
from models.quiz_question import QuizQuestion

QUESTION_POOL = []
UNUSED_QUESTIONS = []

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
    global QUESTION_POOL, UNUSED_QUESTIONS

    # Load all questions only once
    if not QUESTION_POOL:
        QUESTION_POOL = [QuizQuestion.from_dict(q) for q in load_json(QUIZ_QUESTIONS_FILE)]

    # Filter by topic if needed
    if topic:
        filtered = [q for q in QUESTION_POOL if q.topic == topic]
        if not filtered:
            raise ValueError(f"No quiz questions found for topic: {topic}")

        # Create unused list if empty
        if not UNUSED_QUESTIONS:
            UNUSED_QUESTIONS = filtered.copy()

    else:
        # No topic → use full pool
        if not UNUSED_QUESTIONS:
            UNUSED_QUESTIONS = QUESTION_POOL.copy()

    # Pick a random question from unused pool
    q = random.choice(UNUSED_QUESTIONS)

    # Remove it so it won't repeat
    UNUSED_QUESTIONS.remove(q)

    # Return quiz object
    return q

# Alias for compatibility with other parts of your app
generate_open_question = generate_flashcard


# Example usage (you can remove this in production)
if __name__ == "__main__":
    print("Flashcard:", generate_flashcard())
    print("Quiz question:", generate_quiz_question())
    print("Open question:", generate_open_question())