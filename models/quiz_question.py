from typing import List, Optional

class QuizQuestion:
    def __init__(
        self,
        id: int,
        topic: str,
        question: str,
        options: List[str],
        correct: str,
        explanation: Optional[str] = None
    ):
        self.id = id
        self.topic = topic
        self.question = question
        self.options = options
        self.correct = correct
        self.explanation = explanation

    @classmethod
    def from_dict(cls, data: dict) -> "QuizQuestion":
        return cls(
            id=data["id"],
            topic=data["topic"],
            question=data["question"],
            options=data["options"],
            correct=data["correct"],
            explanation=data.get("explanation")
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "topic": self.topic,
            "question": self.question,
            "options": self.options,
            "correct": self.correct,
            "explanation": self.explanation,
        }

    def __str__(self):
        return f"QuizQuestion(id={self.id}, topic='{self.topic}', question='{self.question}')"

    def is_correct(self, selected_option: str) -> bool:
        """
        Checks if the selected option (e.g., 'a', 'b', 'c', etc.) is correct.
        You can pass either the letter or the option string itself.
        """
        # Accepts both letter ('a'/'A') and 'A.' or the full option string
        answer_letter = self.correct.lower()
        if selected_option.lower() == answer_letter:
            return True
        if selected_option.strip().lower().startswith(answer_letter):
            return True
        return False