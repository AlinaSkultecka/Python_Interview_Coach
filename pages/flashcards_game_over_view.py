from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt


class FlashcardsGameOverView(QWidget):
    """
    Separate window shown after all flashcards have been completed.
    Matches the style of other screens (top bar + gradient).
    """

    def __init__(self, main_menu):
        super().__init__()

        self.main_menu = main_menu

        self.setWindowTitle("Flashcards Completed")
        self.setFixedSize(360, 640)

        # Outer layout
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ======================================================
        # TOP BAR
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
        # CONTENT AREA (gradient)
        # ======================================================
        content = QWidget()
        content.setObjectName("Root")

        root = QVBoxLayout(content)
        root.setContentsMargins(20, 40, 20, 20)
        root.setSpacing(20)

        outer.addWidget(content)

        # ======================================================
        # CENTER MESSAGE
        # ======================================================
        root.addStretch()

        title = QLabel("Bravo!")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 48px; font-weight: 800;")
        root.addWidget(title)

        msg = QLabel("Great job!\nYou finished all flashcards!")
        msg.setAlignment(Qt.AlignCenter)
        msg.setStyleSheet("color: white; font-size: 20px; font-weight: 600;")
        msg.setWordWrap(True)
        root.addWidget(msg)

        root.addStretch()

        # ======================================================
        # STYLE SHEET
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
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ffe066,
                    stop:1 #ffd84d
                );
            }
        """)

    # ======================================================
    # NAVIGATION
    # ======================================================
    def return_to_menu(self):
        self.main_menu.show()
        self.close()