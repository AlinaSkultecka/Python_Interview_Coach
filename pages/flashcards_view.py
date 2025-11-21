from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt

from data.question_generator import generate_flashcard
from pages.ui.flashcard_widget import FlashcardWidget


class FlashcardsView(QWidget):
    """
    Flashcards study screen.
    Displays one card at a time with flip animation to reveal answers.
    """

    def __init__(self, main_menu):
        super().__init__()
        self.main_menu = main_menu

        self.cards = [generate_flashcard() for _ in range(20)]
        self.current_index = 0

        self._configure_window()
        self._build_ui()
        self._apply_styles()

        self.show_card()

    # ======================================================================
    # WINDOW SETUP
    # ======================================================================

    def _configure_window(self):
        """Initial window setup."""
        self.setWindowTitle("Flashcards")
        self.setFixedSize(360, 640)

    # ======================================================================
    # UI BUILDING
    # ======================================================================

    def _build_ui(self):
        """Set up layout and all UI widgets."""

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ------------------------------------------------------------------
        # Top bar
        # ------------------------------------------------------------------
        top_row = QWidget()
        top_row.setObjectName("TopRow")
        top_row.setFixedHeight(60)

        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(16, 12, 16, 12)

        # Return to menu
        self.btn_back = QPushButton("Return to Menu")
        self.btn_back.setObjectName("BackBtn")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.clicked.connect(self.return_to_menu)

        # Counter label (1/20)
        self.counter_label = QLabel(self._counter_text())
        self.counter_label.setObjectName("Score")

        top_layout.addWidget(self.btn_back)
        top_layout.addStretch()
        top_layout.addWidget(self.counter_label)

        outer.addWidget(top_row)

        # ------------------------------------------------------------------
        # Gradient content area
        # ------------------------------------------------------------------
        content = QWidget()
        content.setObjectName("Root")

        root = QVBoxLayout(content)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(8)

        outer.addWidget(content)

        # ------------------------------------------------------------------
        # Flashcard
        # ------------------------------------------------------------------
        self.card = FlashcardWidget()
        self.card.face.setFixedSize(320, 340)

        root.addSpacerItem(QSpacerItem(0, 70, QSizePolicy.Minimum, QSizePolicy.Fixed))
        root.addWidget(self.card, alignment=Qt.AlignCenter)
        root.addSpacerItem(QSpacerItem(0, 70, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # ------------------------------------------------------------------
        # Next Card Button
        # ------------------------------------------------------------------
        self.btn_next = QPushButton("Next Card")
        self.btn_next.setObjectName("ActionBtn")
        self.btn_next.clicked.connect(self.next_card)

        root.addWidget(self.btn_next)

    # ======================================================================
    # STYLES
    # ======================================================================

    def _apply_styles(self):
        """CSS styling for entire page."""
        self.setStyleSheet("""
            QWidget#TopRow {
                background: white;
            }

            QWidget#Root {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6A9ABE,
                    stop:1 #6456A3
                );
            }

            QLabel#Score {
                color: #333;
                font-weight: bold;
                font-size: 16px;
            }

            QPushButton#BackBtn {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #fff7b1,
                    stop:1 #ffd84d
                );
                color: #3a3500;
                border: none;
                border-radius: 18px;
                padding: 10px;
                font-size: 16px;
                font-weight: 600;
            }

            QPushButton#BackBtn:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ffe066,
                    stop:1 #ffd84d
                );
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

    # ======================================================================
    # LOGIC
    # ======================================================================

    def _counter_text(self):
        """Returns text like '3/20'."""
        return f"{self.current_index + 1}/{len(self.cards)}"

    def show_card(self):
        """Loads the current card into the UI."""
        card_data = self.cards[self.current_index]
        question = card_data.question.strip()

        # Capitalize first letter
        formatted_question = question[0].upper() + question[1:] if question else question

        self.card.set_front_text(formatted_question)
        self.card.set_back_text(card_data.answer)
        self.card.show_front()

        # Title: "Question 5"
        self.card.title_label.setText(f"Question {self.current_index + 1}")

        # Update counter at top-right
        self.counter_label.setText(self._counter_text())

    def next_card(self):
        """Moves to the next flashcard (loops)."""
        self.current_index = (self.current_index + 1) % len(self.cards)
        self.show_card()

    def return_to_menu(self):
        """Return to main menu."""
        self.main_menu.show()
        self.close()