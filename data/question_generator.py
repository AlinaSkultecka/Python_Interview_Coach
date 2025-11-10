import random

MOCK_QUIZ_QUESTIONS = [
    {
        "question": "What is the output of print(2 * 3)?",
        "options": ["A. 5", "B. 6", "C. 23"],
        "correct": "B",
        "explanation": "2 * 3 is 6."
    },
    {
        "question": "Which data type is immutable in Python?",
        "options": ["A. List", "B. Dictionary", "C. Tuple"],
        "correct": "C",
        "explanation": "Tuples cannot be changed after creation."
    },
]

def generate_quiz_question(topic="Python basics", difficulty="beginner"):
    return random.choice(MOCK_QUIZ_QUESTIONS)

MOCK_OPEN_QUESTIONS = [
    {
        "question": "Explain the difference between a list and a tuple.",
        "answer": "A list is mutable; a tuple is immutable."
    },
    {
        "question": "What is PEP8?",
        "answer": "PEP8 is the style guide for Python code."
    },
]

def generate_open_question(topic="Python basics", difficulty="beginner"):
    return random.choice(MOCK_OPEN_QUESTIONS)