# pages/ui/answer_button.py
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal


class AnswerButton(QFrame):
    """
    Custom answer button used in the quiz.
    Supports:
    - Click signal
    - Correct/wrong visual states
    - Selected state
    - Smooth styled-background rounded card
    """

    clicked = Signal()

    def __init__(self, text: str = "", parent=None):
        super().__init__(parent)

        self._build_ui(text)
        self._apply_styles()

    # ======================================================================
    # UI SETUP
    # ======================================================================

    def _build_ui(self, text: str):
        """Create layout and internal label."""
        self.setObjectName("AnswerButton")
        self.setCursor(Qt.PointingHandCursor)

        # Needed so CSS border-radius and background work correctly
        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setAlignment(Qt.AlignVCenter)

        self.label = QLabel(text, self)
        self.label.setObjectName("AnswerText")
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

    # ======================================================================
    # STYLE RULES
    # ======================================================================

    def _apply_styles(self):
        """Apply visual appearance (CSS)."""
        self.setStyleSheet("""
            QFrame#AnswerButton {
                background: white;
                border-radius: 22px;
                border: 1px solid #e8eaf0;
                min-height: 44px;
                transition: background 150ms ease;
            }

            QFrame#AnswerButton:hover {
                background: #f1f4ff;
            }

            /* Answer correctness feedback */
            QFrame#AnswerButton[state="correct"] {
                background: #9FE69F;
                border: 1px solid #66c066;
            }
            QFrame#AnswerButton[state="wrong"] {
                background: #FF8E8E;
                border: 1px solid #d35e5e;
            }

            /* Faded appearance when disabled */
            QFrame#AnswerButton:disabled {
                opacity: 0.7;
            }

            QLabel#AnswerText {
                font-size: 16px;
                color: #244;
                background: transparent;
            }
        """)

    # ======================================================================
    # STATE CONTROLS
    # ======================================================================

    def setText(self, text: str):
        """Update the label text."""
        self.label.setText(text)

    def setSelected(self, selected: bool):
        """For future styling use: visually mark as selected."""
        self.setProperty("selected", selected)
        self._refresh_style()

    def setState(self, state: str | None):
        """
        Set visual correctness:
        - 'correct'
        - 'wrong'
        - None → clear state
        """
        self.setProperty("state", state or "")
        self._refresh_style()

    def _refresh_style(self):
        """Forces Qt to reapply styles after property changes."""
        self.style().unpolish(self)
        self.style().polish(self)

    # ======================================================================
    # EVENTS
    # ======================================================================

    def mousePressEvent(self, event):
        """Emit a clean clicked signal on left mouse button."""
        if event.button() == Qt.LeftButton:
            self.clicked.emit()