from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

from pages.ui.big_level_button import GradientCardButton
from .play_quiz_view import PlayQuizView
from .flashcards_view import FlashcardsView


class MainMenuView(QWidget):
    """
    Main menu screen shown after login.
    Displays greeting and navigation choices for quiz or flashcards.
    """

    def __init__(self, username: str):
        super().__init__()
        self.username = username

        self._configure_window()
        self._build_ui()

    # ======================================================================
    # WINDOW SETUP
    # ======================================================================

    def _configure_window(self):
        """Basic window setup (size, background, title)."""
        self.setWindowTitle("Main Menu")
        self.setFixedSize(360, 640)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#FFFFFF"))
        self.setPalette(palette)

    # ======================================================================
    # UI BUILDING
    # ======================================================================

    def _build_ui(self):
        """Builds all visual UI components for the main menu."""
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(20, 60, 20, 10)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)

        # --- Greeting ------------------------------------------------------
        hi_user = QLabel(f"Hi, {self.username}")
        hi_user.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #4C4982;
        """)
        hi_user.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(hi_user, alignment=Qt.AlignLeft)

        # --- Header Block (Large Title + Subtitle) -------------------------
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(4)

        welcome = QLabel("Let's play")
        welcome.setObjectName("MenuTitle")
        welcome.setAlignment(Qt.AlignLeft)
        welcome.setStyleSheet("""
            font-size: 50px;
            font-weight: bold;
            color: #4C4982;
        """)

        choose = QLabel("Choose your category")
        choose.setObjectName("MenuSubtitle")
        choose.setAlignment(Qt.AlignLeft)
        choose.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #4C4982;
        """)

        header_layout.addWidget(welcome)
        header_layout.addWidget(choose)

        main_layout.addWidget(header, alignment=Qt.AlignLeft)

        # --- Buttons (Quiz / Flashcards) ----------------------------------
        btn_play = GradientCardButton(
            "Level 1", "Play a Quiz",
            "#D959A8", "#D95968",
            image_path="brain.png"
        )
        btn_play.clicked.connect(self.open_play_quiz)
        main_layout.addWidget(btn_play)

        btn_flashcards = GradientCardButton(
            "Level 2", "Flashcards",
            "#6A9ABE", "#6456A3",
            image_path="flash-cards.png"
        )
        btn_flashcards.clicked.connect(self.open_flashcards)
        main_layout.addWidget(btn_flashcards)

        # Push UI upwards slightly (visual balance)
        main_layout.addStretch(1)

        outer_layout.addLayout(main_layout)

    # ======================================================================
    # NAVIGATION
    # ======================================================================

    def open_play_quiz(self):
        """Open the Quiz window and hide the menu."""
        self.play_quiz_window = PlayQuizView(main_menu=self)
        self.play_quiz_window.show()
        self.hide()

    def open_flashcards(self):
        """Open the Flashcards window and hide the menu."""
        self.flashcards_window = FlashcardsView(main_menu=self)
        self.flashcards_window.show()
        self.hide()