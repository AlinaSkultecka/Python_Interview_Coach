from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt

from data.question_generator import generate_flashcard
from pages.ui.flashcard_widget import FlashcardWidget


class FlashcardsView(QWidget):
    def __init__(self, main_menu):
        super().__init__()
        self.main_menu = main_menu
        self.setWindowTitle("Flashcards")
        self.setFixedSize(360, 640)

        # Load flashcards
        self.cards = [generate_flashcard() for _ in range(20)]
        self.current_index = 0

        # ===========================================================
        # OUTER FRAME (Top bar + content area)
        # ===========================================================
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ===========================================================
        # ROW 1: TOP WHITE BAR
        # ===========================================================
        top_row = QWidget()
        top_row.setObjectName("TopRow")
        top_row.setFixedHeight(60)

        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(16, 12, 16, 12)

        # Back button
        self.btn_back = QPushButton("Return to Menu")
        self.btn_back.setObjectName("BackBtn")
        self.btn_back.clicked.connect(self.return_to_menu)
        self.btn_back.setCursor(Qt.PointingHandCursor)

        # Counter
        self.counter_label = QLabel(self._counter_text())
        self.counter_label.setObjectName("Score")

        top_layout.addWidget(self.btn_back)
        top_layout.addStretch()
        top_layout.addWidget(self.counter_label)

        outer.addWidget(top_row)

        # ===========================================================
        # ROW 2: CONTENT AREA — Gradient background
        # ===========================================================
        content = QWidget()
        content.setObjectName("Root")

        root = QVBoxLayout(content)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(8)

        outer.addWidget(content)

        # ===========================================================
        # FLASHCARD FLIP WIDGET
        # ===========================================================
        self.card = FlashcardWidget()
        self.card.face.setFixedSize(320, 340)  # larger card
        root.addSpacerItem(QSpacerItem(0, 70, QSizePolicy.Minimum, QSizePolicy.Fixed))
        root.addWidget(self.card, alignment=Qt.AlignCenter)
        root.addSpacerItem(QSpacerItem(0, 70, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # ------------------------ Next button -----------------------
        self.btn_next = QPushButton("Next Card")
        self.btn_next.setObjectName("ActionBtn")
        self.btn_next.clicked.connect(self.next_card)
        root.addWidget(self.btn_next)

        # ===========================================================
        # STYLES — Matches PlayQuizView
        # ===========================================================
        self.setStyleSheet("""
            QWidget#TopRow {
                background: white;
            }

            QWidget#Root {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                                            stop:0 #6A9ABE, stop:1 #6456A3);
            }

            QLabel#Score {
                color: #333;
                font-weight: bold;
                font-size: 16px;
            }

            QPushButton#BackBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #fff7b1, stop:1 #ffd84d);
                color: #3a3500;
                border: none;
                border-radius: 18px;
                padding: 10px;
                font-size: 16px;
                font-weight: 600;
            }

            QPushButton#BackBtn:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                                            stop:0 #ffe066, stop:1 #ffd84d);
            }

            QPushButton#ActionBtn {
                background: white;
                color: #222;
                border: none;
                border-radius: 22px;
                padding: 12px;
                font-size: 17px;
                font-weight: 600;
            }

            QPushButton#ActionBtn:hover {
                background: #f2f2f2;
            }

            QWidget#Flashcard {
                background: white;
                border-radius: 22px;
            }

            QLabel#FlashcardText {
                color: #222;
                font-size: 18px;
                font-weight: 600;
            }
           QLabel#FlashHint {
                color: #999;
                font-size: 13px;
                font-weight: 500;
            }
           QLabel#FlashTitle {
                color: #555;
                font-size: 16px;
                font-weight: 700;
                padding-bottom: 6px;
            }
        """)

        # Load first card
        self.show_card()

    # ===========================================================
    # LOGIC
    # ===========================================================
    def _counter_text(self):
        return f"{self.current_index + 1}/{len(self.cards)}"

    def show_card(self):
        card = self.cards[self.current_index]
        question = card.question.strip()

        self.card.set_front_text(question[0].upper() + question[1:])
        self.card.set_back_text(card.answer)
        self.card.show_front()

        # NEW: update title
        self.card.title_label.setText(f"Question {self.current_index + 1}")

        self.counter_label.setText(self._counter_text())

    def next_card(self):
        self.current_index = (self.current_index + 1) % len(self.cards)
        self.show_card()

    def return_to_menu(self):
        self.main_menu.show()
        self.close()
