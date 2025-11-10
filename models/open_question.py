class OpenQuestion:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    @classmethod
    def from_dict(cls, d):
        return cls(
            question=d["question"],
            answer=d.get("answer", "")
        )