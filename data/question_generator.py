"""
Utility functions for loading and generating:
- flashcards (OpenQuestion)
- multiple-choice quiz questions (QuizQuestion)

Supports optional topic filtering and ensures quiz questions
do not repeat until the full pool is exhausted.
"""

import os
import json
import random

from models.flashcards_questions import OpenQuestion
from models.quiz_question import QuizQuestion


# ----------------------------------------------------------------------
# Internal pools (for non-repeating quiz questions)
# ----------------------------------------------------------------------

QUESTION_POOL = []      # Loaded once from JSON
UNUSED_QUESTIONS = []   # Rotates until empty


# ----------------------------------------------------------------------
# File paths
# ----------------------------------------------------------------------

FLASHCARDS_FILE = os.path.join("data", "quiz_flashcards", "flashcards.json")
QUIZ_QUESTIONS_FILE = os.path.join("data", "quiz_flashcards", "quiz_questions.json")


# ======================================================================
# DATA LOADING HELPERS
# ======================================================================

def load_json(path: str) -> list:
    """Load and return JSON content from a file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ======================================================================
# FLASHCARDS
# ======================================================================

def generate_flashcard(topic: str | None = None) -> OpenQuestion:
    """
    Returns a random flashcard.
    If `topic` is provided, select only cards from that topic.
    """
    flashcards = load_json(FLASHCARDS_FILE)

    # Topic filtering
    if topic:
        flashcards = [fc for fc in flashcards if fc.get("topic") == topic]
        if not flashcards:
            raise ValueError(f"No flashcards found for topic: {topic}")

    return OpenQuestion.from_dict(random.choice(flashcards))


# Alias for naming consistency
generate_open_question = generate_flashcard


# ======================================================================
# QUIZ QUESTIONS
# ======================================================================

def generate_quiz_question(topic: str | None = None) -> QuizQuestion:
    """
    Returns a random QuizQuestion, ensuring no repeats until the pool is exhausted.

    If topic is provided, uses only questions from that topic,
    and creates a separate unused list for that subset.
    """
    global QUESTION_POOL, UNUSED_QUESTIONS

    # Load full question pool once
    if not QUESTION_POOL:
        raw = load_json(QUIZ_QUESTIONS_FILE)
        QUESTION_POOL = [QuizQuestion.from_dict(q) for q in raw]

    # If topic is provided, filter pool for that topic
    if topic:
        filtered = [q for q in QUESTION_POOL if q.topic == topic]
        if not filtered:
            raise ValueError(f"No quiz questions found for topic: {topic}")

        # Reset unused list if needed (topic-specific mode)
        if not UNUSED_QUESTIONS:
            UNUSED_QUESTIONS = filtered.copy()

    else:
        # No topic → use the full pool
        if not UNUSED_QUESTIONS:
            UNUSED_QUESTIONS = QUESTION_POOL.copy()

    # Choose 1 question from unused
    question = random.choice(UNUSED_QUESTIONS)
    UNUSED_QUESTIONS.remove(question)

    return question


# ======================================================================
# DEBUG USAGE
# ======================================================================

if __name__ == "__main__":
    print("Flashcard example:", generate_flashcard())
    print("Quiz question example:", generate_quiz_question())
    print("Open question example:", generate_open_question())