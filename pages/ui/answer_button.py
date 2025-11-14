# pages/ui/answer_button.py
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal

class AnswerButton(QFrame):
    clicked = Signal()

    def __init__(self, text: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("AnswerButton")
        self.setCursor(Qt.PointingHandCursor)
        # ensure this widget paints its own background (needed for border-radius)
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Inner layout (padding)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setAlignment(Qt.AlignVCenter)

        self.label = QLabel(text, self)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("font-size: 16px; color: #244; background: transparent;")
        layout.addWidget(self.label)

        # Styles
        self.setStyleSheet("""
            QFrame#AnswerButton {
                background: white;
                border-radius: 22px;
                border: 1px solid #e8eaf0;
                min-height: 44px;
            }
            QFrame#AnswerButton:hover {
                background: #f1f4ff;
            }
            /* NEW: correctness states for transient feedback */
            QFrame#AnswerButton[state="correct"] {
                background: #9FE69F;
            }
            QFrame#AnswerButton[state="wrong"] {
                background: #FF8E8E;
            }
            QFrame#AnswerButton:disabled {
                opacity: 0.75;
            }
        """)

    def setText(self, text: str):
        self.label.setText(text)

    def setSelected(self, selected: bool):
        self.setProperty("selected", selected)
        self.style().unpolish(self)
        self.style().polish(self)

    def setState(self, state: str | None):
        """state: 'correct', 'wrong', or None to clear."""
        self.setProperty("state", state or "")
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()