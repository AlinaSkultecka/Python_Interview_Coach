from typing import List, Optional


class QuizQuestion:
    """
    Represents a multiple-choice quiz question.

    Includes:
    - topic
    - question text
    - list of 4 options (strings)
    - correct answer letter ('a'/'b'/'c'/'d')
    - optional explanation text (shown on wrong answers)
    """

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

    # --------------------------------------------------------------
    # Converters
    # --------------------------------------------------------------

    @classmethod
    def from_dict(cls, data: dict) -> "QuizQuestion":
        """Create a QuizQuestion from a dictionary."""
        return cls(
            id=data["id"],
            topic=data["topic"],
            question=data["question"],
            options=data["options"],
            correct=data["correct"],
            explanation=data.get("explanation"),
        )

    def to_dict(self) -> dict:
        """Serialize the question to a dictionary."""
        return {
            "id": self.id,
            "topic": self.topic,
            "question": self.question,
            "options": self.options,
            "correct": self.correct,
            "explanation": self.explanation,
        }

    # --------------------------------------------------------------
    # Introspection & logic
    # --------------------------------------------------------------

    def __str__(self):
        return f"QuizQuestion(id={self.id}, topic='{self.topic}', question='{self.question}')"

    def is_correct(self, selected_option: str) -> bool:
        """
        Returns True if the given selected option is correct.

        Accepts:
        - letter ("a", "b", ...)
        - letter with formatting ("A.", "b)")
        - full option string ("print()", etc.)
        """

        correct_letter = self.correct.lower()
        choice = selected_option.strip().lower()

        # Exact letter match
        if choice == correct_letter:
            return True

        # If option begins with the correct letter (like "a. something")
        if choice.startswith(correct_letter):
            return True

        return False