from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QSpacerItem, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor


class EntranceWindow(QWidget):
    """
    The very first screen of the app.
    Welcomes the user and collects their name inside a centered card.
    """

    def __init__(self):
        super().__init__()

        self._configure_window()
        self._build_ui()

    # ======================================================================
    # WINDOW SETUP
    # ======================================================================

    def _configure_window(self):
        """Basic window properties and background gradient."""
        self.setWindowTitle("Welcome")
        self.setFixedSize(360, 640)

        # Smooth gradient background
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #E5FCC2,
                    stop:1 #C2E5FC
                );
            }
        """)

    # ======================================================================
    # UI BUILDING
    # ======================================================================

    def _build_ui(self):
        """Constructs the entire entrance layout."""

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 70, 20, 130)

        # --- Heading --------------------------------------------------------
        welcome = QLabel("Welcome to")
        welcome.setAlignment(Qt.AlignHCenter)
        welcome.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #4C4982;
            background: transparent;
        """)
        layout.addWidget(welcome)

        # Main title (multi-line)
        title = QLabel("PYTHON\nINTERVIEW\nCOACH")
        title.setAlignment(Qt.AlignHCenter)
        title.setWordWrap(True)
        title.setStyleSheet("""
            font-size: 44px;
            font-weight: bold;
            color: #4C4982;
            background: transparent;
        """)
        layout.addWidget(title)

        # Spacer before card
        layout.addSpacerItem(
            QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)
        )

        # --- Card container -------------------------------------------------
        card = QFrame()
        card.setObjectName("EntranceCard")
        card.setFixedWidth(300)
        card.setStyleSheet("""
            QFrame#EntranceCard {
                background: white;
                border-radius: 18px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(14)
        card_layout.setContentsMargins(20, 20, 20, 20)

        # --- Card Contents --------------------------------------------------
        prompt = QLabel("Enter your name:")
        prompt.setAlignment(Qt.AlignLeft)
        prompt.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #4C4982;
            background: white;
        """)
        card_layout.addWidget(prompt)

        # Username input field
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Your name")
        self.name_input.setMaxLength(32)
        self.name_input.setFixedHeight(40)
        self.name_input.setStyleSheet("""
            font-size: 18px;
            padding-left: 10px;
            background: white;
            border: none;             
            outline: none;          
        """)
        card_layout.addWidget(self.name_input)

        # Continue button
        self.btn_continue = QPushButton("Continue")
        self.btn_continue.setFixedHeight(40)
        self.btn_continue.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            background-color: #4C4982;
            color: white;
        """)
        card_layout.addWidget(self.btn_continue)

        # Add card centered
        layout.addWidget(card, alignment=Qt.AlignHCenter)

        self.setLayout(layout)