from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

class EntranceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.setFixedSize(360, 640)

        # Set background gradient from #FCF6C2 (top) to #E5FCC2 (bottom)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #E5FCC2,
                    stop:1 #C2E5FC
                );
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 70, 20, 130)

        # Welcome to Heading
        welcome = QLabel("Welcome to")
        welcome.setStyleSheet("font-size: 20px; font-weight: bold; color: #4C4982; background: transparent")
        welcome.setAlignment(Qt.AlignHCenter)
        layout.addWidget(welcome, alignment=Qt.AlignHCenter)

        # Game name title heading
        gameTitle = QLabel("PYTHON\nINTERVIEW\nCOACH")
        gameTitle.setStyleSheet("font-size: 44px; font-weight: bold; color: #4C4982; background: transparent")
        gameTitle.setAlignment(Qt.AlignHCenter)
        gameTitle.setWordWrap(True)
        layout.addWidget(gameTitle, alignment=Qt.AlignHCenter)

        # Extra space before the card
        layout.addSpacerItem(QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # White card for user entrance
        card = QFrame()
        card.setStyleSheet("""
            background: white;
            border-radius: 18px;
        """)
        card.setFixedWidth(300)  # You can adjust width here

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(14)
        card_layout.setContentsMargins(20, 20, 20, 20)

        # Username entrance inside the card
        label = QLabel("Enter your name:")
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        card_layout.addWidget(label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Your name")
        self.name_input.setMaxLength(32)
        self.name_input.setFixedHeight(40)
        self.name_input.setStyleSheet("font-size: 18px; padding-left: 10px;")
        card_layout.addWidget(self.name_input)

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

        # Add the card to the main layout, centered
        layout.addWidget(card, alignment=Qt.AlignHCenter)

        self.setLayout(layout)