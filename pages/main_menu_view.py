from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QFrame, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

import widgets.big_level_button
from .play_quiz_view import PlayQuizView
from .flashcards_view import FlashcardsView

class MainMenuView(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Main Menu")
        self.setFixedSize(360, 640)

        # Set window background to white
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor("#FFFFFF"))  # White background
        self.setPalette(pal)

        # OUTER layout without margin
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(20, 60, 20, 10)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)

        # Hi, user label at the very top
        hi_user = QLabel(f"Hi, {self.username}")
        hi_user.setStyleSheet("font-size: 16px; font-weight: bold; color: #4C4982;")
        hi_user.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(hi_user, alignment=Qt.AlignLeft)

        # --- Tight header block: "Let's play" + "Choose your category" ---
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(4)  # << controls the gap between the two lines

        # Welcome to Heading
        welcome = QLabel("Let's play")
        welcome.setStyleSheet("font-size: 50px; font-weight: bold; color: #4C4982")
        welcome.setAlignment(Qt.AlignLeft )

        # Text choose your category
        choose = QLabel("Choose your category")
        choose.setStyleSheet("font-size: 20px; font-weight: bold; color: #4C4982")
        choose.setAlignment(Qt.AlignLeft)
        choose.setMinimumHeight(70)

        welcome.setContentsMargins(0, 0, 0, 0)
        choose.setContentsMargins(0, 0, 0, 0)

        header_layout.addWidget(welcome)
        header_layout.addWidget(choose)

        main_layout.addWidget(header, alignment=Qt.AlignLeft)

        # Play Quiz Button
        btn_play = widgets.big_level_button.GradientCardButton(
            "Level 1", "Play a Quiz",
            "#D959A8", "#D95968",
            image_path="brain.png"  # optional
        )
        btn_play.clicked.connect(self.open_play_quiz)
        main_layout.addWidget(btn_play)

        # Flashcards Button
        btn_flashcards = widgets.big_level_button.GradientCardButton(
            "Level 2", "Flashcards",
            "#6A9ABE", "#6456A3",
            image_path="flash-cards.png"  # optional
        )
        btn_flashcards.clicked.connect(self.open_flashcards)
        main_layout.addWidget(btn_flashcards)





        main_layout.addStretch(1)  # Push everything up for better look

        # Set the layout directly
        outer_layout.addLayout(main_layout)

    def open_play_quiz(self):
        self.play_quiz_window = PlayQuizView(main_menu=self)
        self.play_quiz_window.show()
        self.hide()

    def open_flashcards(self):
        self.flashcards_window = FlashcardsView(main_menu=self)
        self.flashcards_window.show()
        self.hide()