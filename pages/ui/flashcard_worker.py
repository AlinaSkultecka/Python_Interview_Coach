# pages/ui/flashcard_worker.py

from PySide6.QtCore import QObject, Signal

class FlashcardWorker(QObject):
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, topic):
        super().__init__()
        self.topic = topic

    def run(self):
        try:
            from data.ai_flashcards_generator import generate_ai_flashcards
            cards = generate_ai_flashcards(self.topic)
            self.finished.emit(cards)
        except Exception as e:
            self.error.emit(str(e))