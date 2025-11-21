from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, QThread

from data.ai_flashcards_generator import generate_ai_flashcards
from pages.ui.flashcard_worker import FlashcardWorker
from pages.ui.flashcard_widget import FlashcardWidget
from pages.ui.animated_border_button import AnimatedBorderButton


class FlashcardsAIView(QWidget):
    """
    AI Flashcards screen.
    Step 1: User enters topic.
    Step 2: App generates AI flashcards using GPT-4.1-mini.
    Step 3: User flips through cards similarly to premade mode.
    """

    def __init__(self, main_menu):
        super().__init__()

        self.thread = None
        self.main_menu = main_menu
        self.cards = []
        self.current_index = 0

        self.setWindowTitle("AI Flashcards")
        self.setFixedSize(360, 640)

        # ------------------------------------------------------------------
        # LAYOUT
        # ------------------------------------------------------------------
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Top bar -----------------------------------------------------------
        top_row = QWidget()
        top_row.setObjectName("TopRow")
        top_row.setFixedHeight(60)

        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(16, 12, 16, 12)

        btn_back = QPushButton("Return to Menu")
        btn_back.setObjectName("BackBtn")
        btn_back.setCursor(Qt.PointingHandCursor)
        btn_back.clicked.connect(self.return_to_menu)

        top_layout.addWidget(btn_back)
        top_layout.addStretch()
        outer.addWidget(top_row)

        # Main content ------------------------------------------------------
        content = QWidget()
        content.setObjectName("Root")
        root = QVBoxLayout(content)
        root.setContentsMargins(20, 10, 20, 0)
        root.setSpacing(10)
        outer.addWidget(content)

        # Title -------------------------------------------------------------
        title = QLabel("AI Flashcards")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 32px; font-weight: 800;")
        root.addWidget(title)

        subtitle = QLabel("Enter a topic below:")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: white; font-size: 16px;")
        root.addWidget(subtitle)

        # Input field -------------------------------------------------------
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("e.g., Python functions")
        self.topic_input.setFixedHeight(45)
        self.topic_input.setStyleSheet("""
            border: none;
            background: white;
            border-radius: 12px;
            padding: 10px;
            font-size: 16px;
        """)
        root.addWidget(self.topic_input)

        # Generate Button (animated border) ---------------------------------
        self.btn_generate = AnimatedBorderButton("Generate Flashcards")
        self.btn_generate.setObjectName("GenerateBtn")
        self.btn_generate.setCursor(Qt.PointingHandCursor)
        self.btn_generate.clicked.connect(self.generate_cards)
        self.btn_generate.setFixedHeight(45)
        root.addWidget(self.btn_generate)

        # Spacer before flashcard -------------------------------------------
        root.addSpacerItem(QSpacerItem(0, 6, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Flashcard Display -------------------------------------------------
        self.flashcard = FlashcardWidget()
        self.flashcard.face.setFixedSize(300, 280)
        self.flashcard.hide()
        root.addWidget(self.flashcard, alignment=Qt.AlignCenter)

        # Spacer after flashcard --------------------------------------------
        root.addSpacerItem(QSpacerItem(0, 6, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Next button -------------------------------------------------------
        self.btn_next = QPushButton("Next")
        self.btn_next.setObjectName("NextBtn")
        self.btn_next.clicked.connect(self.next_card)
        self.btn_next.setFixedHeight(45)
        self.btn_next.hide()
        root.addWidget(self.btn_next)

        root.addStretch()

        # ------------------------------------------------------------------
        # STYLE SHEET
        # ------------------------------------------------------------------
        self.setStyleSheet("""
            QWidget#TopRow { 
                background: white; 
            }

            QWidget#Root {
                background: qlineargradient(
                    x1:0,y1:0,x2:0,y2:1,
                    stop:0 #6A9ABE, stop:1 #6456A3
                );
            }

            QPushButton#BackBtn {
                background: qlineargradient(
                    x1:0,y1:0,x2:1,y2:0,
                    stop:0 #fff7b1, stop:1 #ffd84d
                );
                border: none;
                border-radius: 18px;
                padding: 10px;
                font-size: 16px;
                font-weight: 600;
                color: #3a3500;
            }
            QPushButton#BackBtn:hover {
                background: qlineargradient(
                    x1:0,y1:0,x2:1,y2:0,
                    stop:0 #ffe066, stop:1 #ffd84d
                );
            }

            QPushButton#GenerateBtn {
                background: #6456A3;
                color: white;
                border: none;
                border-radius: 22px;
                padding: 12px;
                font-size: 18px;
                font-weight: 700;
            }
            QPushButton#GenerateBtn:hover {
                background: #7263B4;
            }

            QPushButton#NextBtn {
                background: white;
                color: #222;
                border: none;
                border-radius: 22px;
                padding: 12px;
                font-size: 18px;
                font-weight: 700;
            }
            QPushButton#NextBtn:hover {
                background: #f1f1f1;
            }

            QWidget#Flashcard {
                background: white;
                border-radius: 22px;
            }
            QLabel#FlashcardText {
                color: #222;
                font-size: 16px;
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

    # ------------------------------------------------------------------
    # LOGIC
    # ------------------------------------------------------------------
    def generate_cards(self):
        # If user leaves it empty, default to "any"
        topic = self.topic_input.text().strip()
        if not topic:
            topic = "any"

        self.btn_generate.setEnabled(False)
        self.btn_generate.setLoading(True)

        self.thread = QThread()
        self.worker = FlashcardWorker(topic)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_flashcards_ready)
        self.worker.error.connect(self.on_flashcards_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_flashcards_ready(self, cards):
        self.cards = cards
        self.btn_generate.setEnabled(True)
        self.btn_generate.setLoading(False)
        if not self.cards:
            QMessageBox.warning(self, "No cards", "The AI did not return any flashcards.")
            return
        self.current_index = 0
        self.show_card()
        self.flashcard.show()
        self.btn_next.show()

    def on_flashcards_error(self, message):
        self.btn_generate.setEnabled(True)
        self.btn_generate.setLoading(False)
        QMessageBox.critical(self, "Error", message)

    def show_card(self):
        card = self.cards[self.current_index]
        self.flashcard.set_front_text(card.question)
        self.flashcard.set_back_text(card.answer)
        self.flashcard.show_front()

    def next_card(self):
        self.current_index += 1

        if self.current_index >= len(self.cards):
            QMessageBox.information(self, "Done", "You reviewed all AI-generated flashcards.")
            self.return_to_menu()
            return

        self.show_card()

    def return_to_menu(self):
        self.main_menu.show()
        self.close()

