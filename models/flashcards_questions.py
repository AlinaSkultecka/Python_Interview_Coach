class OpenQuestion:
    """
    Represents an open-ended question (free text answer),
    used for flashcards or written-response quizzes.
    """

    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer

    @classmethod
    def from_dict(cls, data: dict) -> "OpenQuestion":
        """Create an OpenQuestion from a dictionary."""
        return cls(
            question=data["question"],
            answer=data.get("answer", "")
        )

    def to_dict(self) -> dict:
        """Serialize the question to a dictionary."""
        return {
            "question": self.question,
            "answer": self.answer,
        }

    def __str__(self):
        return f"OpenQuestion(question='{self.question}')"