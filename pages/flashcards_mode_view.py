from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt


class FlashcardsModeView(QWidget):
    """
    Window shown between the Main Menu and the Flashcards gameplay.
    Lets the user choose:
        - Premade flashcards
        - AI-generated flashcards (future feature)
    """

    def __init__(self, main_menu):
        super().__init__()

        self.main_menu = main_menu

        self.setWindowTitle("Choose Flashcards Mode")
        self.setFixedSize(360, 640)

        # ======================================================
        # OUTER LAYOUT
        # ======================================================
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ======================================================
        # TOP BAR (same as all screens)
        # ======================================================
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

        # ======================================================
        # CONTENT AREA — GRADIENT BACKGROUND
        # ======================================================
        content = QWidget()
        content.setObjectName("Root")

        root = QVBoxLayout(content)
        root.setContentsMargins(20, 60, 20, 20)
        root.setSpacing(15)

        outer.addWidget(content)

        # ======================================================
        # TITLE
        # ======================================================
        title = QLabel("Choose Mode")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 38px; font-weight: 800;")
        root.addWidget(title)

        subtitle = QLabel("How would you like to play?")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: white; font-size: 18px; font-weight: 600;")
        root.addWidget(subtitle)

        root.addStretch()

        # ======================================================
        # PLAY PREMADE FLASHCARDS BUTTON
        # ======================================================
        btn_premade = QPushButton("Play Premade Flashcards")
        btn_premade.setObjectName("ActionBtn")
        btn_premade.setCursor(Qt.PointingHandCursor)
        btn_premade.setFixedHeight(70)
        btn_premade.setMinimumWidth(300)
        btn_premade.clicked.connect(self.open_premade)
        root.addWidget(btn_premade)

        # ======================================================
        # PLAY AI-GENERATED FLASHCARDS BUTTON
        # ======================================================
        btn_ai = QPushButton("Play AI Flashcards")
        btn_ai.setObjectName("ActionBtn")
        btn_ai.setCursor(Qt.PointingHandCursor)
        btn_ai.setFixedHeight(70)
        btn_ai.setMinimumWidth(300)
        btn_ai.clicked.connect(self.open_ai_flashcards)
        root.addWidget(btn_ai)

        root.addStretch()

        # ======================================================
        # STYLESHEET (same as Game Over, but purple/blue gradient)
        # ======================================================
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
                    x1:0,y1:0,x2:1,y2:0,
                    stop:0 #ffe066, stop:1 #ffd84d
                );
            }

            QPushButton#ActionBtn {
                background: white;
                color: #222;
                border: none;
                border-radius: 22px;
                padding: 12px;
                font-size: 20px;
                font-weight: 600;
            }

            QPushButton#ActionBtn:hover {
                background: #f1f1f1;
            }
        """)

    # ======================================================
    # BUTTON LOGIC
    # ======================================================

    def return_to_menu(self):
        self.main_menu.show()
        self.close()

    def open_premade(self):
        """Opens the standard flashcards view."""
        from .flashcards_view import FlashcardsView
        self.flashcards = FlashcardsView(main_menu=self.main_menu)
        self.flashcards.show()
        self.close()

    def open_ai_flashcards(self):
        from .flashcards_ai_view import FlashcardsAIView
        self.ai_view = FlashcardsAIView(main_menu=self.main_menu)
        self.ai_view.show()
        self.close()