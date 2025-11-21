import json
import os

BEST_SCORE_FILE = os.path.join("data", "quiz_flashcards", "quiz_best_score.json")


def load_best_score() -> int:
    if not os.path.exists(BEST_SCORE_FILE):
        return 0
    try:
        with open(BEST_SCORE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("best_score", 0)
    except:
        return 0


def save_best_score(score: int):
    with open(BEST_SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump({"best_score": score}, f, indent=4)