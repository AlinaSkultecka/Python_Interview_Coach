from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from data.question_generator import generate_flashcard

class FlashcardsView(QWidget):
    def __init__(self, main_menu):
        super().__init__()
        self.main_menu = main_menu
        self.setWindowTitle("Flashcards")
        self.setFixedSize(360, 640)

        self.cards = [generate_flashcard() for _ in range(2)]   # e.g., 2 random cards
        self.current_index = 0

        self.layout = QVBoxLayout()
        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        self.answer_label = QLabel()
        self.answer_label.setStyleSheet("color: gray;")
        self.layout.addWidget(self.answer_label)

        self.btn_show = QPushButton("Show Answer")
        self.btn_show.clicked.connect(self.show_answer)
        self.layout.addWidget(self.btn_show)

        self.btn_next = QPushButton("Next Card")
        self.btn_next.clicked.connect(self.next_card)
        self.layout.addWidget(self.btn_next)

        self.btn_back = QPushButton("Return to Menu")
        self.btn_back.clicked.connect(self.return_to_menu)
        self.layout.addWidget(self.btn_back)

        self.setLayout(self.layout)
        self.show_card()

    def show_card(self):
        card = self.cards[self.current_index]
        self.question_label.setText(card.question)
        self.answer_label.setText("")
        self.btn_show.setEnabled(True)

    def show_answer(self):
        card = self.cards[self.current_index]
        self.answer_label.setText(card.answer)
        self.btn_show.setEnabled(False)

    def next_card(self):
        self.current_index = (self.current_index + 1) % len(self.cards)
        self.show_card()

    def return_to_menu(self):
        self.main_menu.show()
        self.close()