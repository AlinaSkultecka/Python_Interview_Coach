from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton
)
from PySide6.QtCore import Qt


class PlayQuizGameOverView(QWidget):
    """
    Screen shown when the quiz is finished.
    Shows score, congratulation message,
    and a button to restart the quiz.
    """

    def __init__(self, main_menu, score_correct, score_total):
        super().__init__()

        self.main_menu = main_menu
        self.score_correct = score_correct
        self.score_total = score_total

        self.setWindowTitle("Quiz Completed")
        self.setFixedSize(360, 640)

        # ======================================================
        # OUTER LAYOUT
        # ======================================================
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
        # CONTENT AREA (gradient background)
        # ======================================================
        content = QWidget()
        content.setObjectName("Root")

        root = QVBoxLayout(content)
        root.setContentsMargins(20, 60, 20, 20)
        root.setSpacing(20)

        outer.addWidget(content)

        # ======================================================
        # CENTER MESSAGE
        # ======================================================
        bravo = QLabel("Bravo!")
        bravo.setAlignment(Qt.AlignCenter)
        bravo.setStyleSheet("color: white; font-size: 48px; font-weight: 800;")
        root.addWidget(bravo)

        msg = QLabel("Great job!\nYou finished the quiz!")
        msg.setAlignment(Qt.AlignCenter)
        msg.setStyleSheet("color: white; font-size: 20px; font-weight: 600;")
        msg.setWordWrap(True)
        root.addWidget(msg)

        # Score Display
        score_text = QLabel(f"Score: {self.score_correct} / {self.score_total}")
        score_text.setAlignment(Qt.AlignCenter)
        score_text.setStyleSheet("color: white; font-size: 24px; font-weight: 700; margin-top: 10px;")
        root.addWidget(score_text)

        # Restart button
        btn_restart = QPushButton("Play Again")
        btn_restart.setObjectName("ActionBtn")
        btn_restart.setCursor(Qt.PointingHandCursor)
        btn_restart.clicked.connect(self.restart_quiz)
        root.addWidget(btn_restart)

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
                    stop:0 #D959A8,
                    stop:1 #D95968
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

            QPushButton#ActionBtn {
                background: white;
                color: #222;
                border: none;
                border-radius: 22px;
                padding: 12px;
                font-size: 17px;
                font-weight: 600;
                margin-top: 20px;
            }

            QPushButton#ActionBtn:hover {
                background: #f2f2f2;
            }
        """)

    # ======================================================
    # NAVIGATION
    # ======================================================

    def return_to_menu(self):
        self.main_menu.show()
        self.close()

    def restart_quiz(self):
        """Restart the quiz from the beginning."""
        from .play_quiz_view import PlayQuizView

        self.new_quiz = PlayQuizView(main_menu=self.main_menu)
        self.new_quiz.show()
        self.close()