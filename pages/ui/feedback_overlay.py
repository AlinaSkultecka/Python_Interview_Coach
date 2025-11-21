"""
pages/ui/feedback_overlay.py

A reusable centered-overlay component for showing
feedback messages (Correct / Wrong) with a tinted card.

Appears above the parent widget, blocks input underneath,
and closes when user clicks or presses any key.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame,
    QGraphicsDropShadowEffect, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class FeedbackOverlay(QWidget):
    """
    A modal-style overlay that covers its parent and displays
    a centered message card with optional color state:
        - 'correct'
        - 'wrong'
        - None (neutral white card)

    The overlay closes ONLY when the user clicks or presses any key.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._on_close = None

        self._configure_overlay_window()
        self._build_ui()
        self._apply_styles()

        self.hide()

    # ======================================================================
    # OVERLAY CONFIG
    # ======================================================================

    def _configure_overlay_window(self):
        """Basic window properties: frameless, transparent background."""
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAutoFillBackground(False)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setObjectName("OverlayRoot")

    # ======================================================================
    # UI BUILDING
    # ======================================================================

    def _build_ui(self):
        """Creates the centered message card with title/body/hint."""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        # Card (the visible message container)
        self.card = QFrame(self)
        self.card.setObjectName("overlayCard")
        layout.addWidget(self.card, 0, Qt.AlignCenter)

        box = QVBoxLayout(self.card)
        box.setContentsMargins(16, 14, 16, 14)
        box.setSpacing(6)
        box.setAlignment(Qt.AlignCenter)

        # Title
        self.title = QLabel("")
        self.title.setObjectName("overlayTitle")

        # Body text
        self.body = QLabel("")
        self.body.setObjectName("overlayBody")
        self.body.setWordWrap(True)

        # Hint
        self.hint = QLabel("Press any key or click to continue")
        self.hint.setObjectName("overlayHint")

        box.addWidget(self.title)
        box.addWidget(self.body)
        box.addWidget(self.hint)

        # Optional drop shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 70))
        self.card.setGraphicsEffect(shadow)

    # ======================================================================
    # STYLING
    # ======================================================================

    def _apply_styles(self):
        """CSS definitions for overlay and message card."""

        self.setStyleSheet("""
            QWidget#OverlayRoot {
                background: transparent;
            }

            QFrame#overlayCard {
                background: white;
                border-radius: 14px;
            }

            /* Tinted card states */
            QWidget[state="correct"] QFrame#overlayCard {
                background: #9FE69F;
            }
            QWidget[state="wrong"] QFrame#overlayCard {
                background: #FF8E8E;
            }

            QLabel#overlayTitle {
                font-size: 15px;
                font-weight: 700;
                color: #123;
                margin-bottom: 4px;
            }

            QLabel#overlayBody {
                font-size: 14px;
                color: #123;
            }

            QLabel#overlayHint {
                font-size: 12px;
                color: #567;
                margin-top: 8px;
            }
        """)

    # ======================================================================
    # PUBLIC API
    # ======================================================================

    def show_message(self, title: str, text: str, on_close=None, state: str | None = None):
        """
        Display the overlay using the given title/body.

        Parameters:
            title    - Top heading of the card
            text     - Body text (supports multiline)
            on_close - Callback executed after closing overlay
            state    - One of: 'correct', 'wrong', None
        """
        self._on_close = on_close
        self.title.setText(title)
        self.body.setText(text)

        # Apply visual tint state
        self.setProperty("state", state or "")
        self._refresh_style()

        # Ensure overlay covers parent
        parent = self.parentWidget()
        if parent:
            self.setGeometry(0, 0, parent.width(), parent.height())

        # Adjust card width to parent size
        max_card_w = min(int(parent.width() * 0.90), 560)
        self.card.setMaximumWidth(max_card_w)
        self.body.setFixedWidth(max_card_w - 32)

        self.show()
        self.raise_()
        self.setFocus(Qt.ActiveWindowFocusReason)

    # ======================================================================
    # DISMISSAL HANDLING
    # ======================================================================

    def _finish(self):
        """Close overlay and run callback if provided."""
        self.hide()
        cb = self._on_close
        self._on_close = None
        if cb:
            cb()

    def mousePressEvent(self, _event):
        self._finish()

    def keyPressEvent(self, _event):
        self._finish()

    # ======================================================================
    # RESIZING & UTILS
    # ======================================================================

    def resizeEvent(self, _ev):
        """Ensure overlay always fills its parent."""
        parent = self.parentWidget()
        if parent and self.isVisible():
            self.setGeometry(0, 0, parent.width(), parent.height())

    def _refresh_style(self):
        """Force Qt to reapply stylesheet after property changes."""
        self.style().unpolish(self)
        self.style().polish(self)