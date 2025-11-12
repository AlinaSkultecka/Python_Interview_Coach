# pages/ui/feedback_overlay.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QGraphicsDropShadowEffect, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class FeedbackOverlay(QWidget):
    """
    Full-parent overlay with transparent background and a centered white card.
    No wasted space, rounded corners, reliable on Windows.
    Closes ONLY on click or key (no auto-close).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAutoFillBackground(False)
        self.hide()

        # Transparent overlay; only the card is visible
        self.setStyleSheet("""
            QWidget#OverlayRoot { background: transparent; }   /* overlay itself */
            QFrame#overlayCard {
                background: white;
                border-radius: 14px;
            }
            QLabel#overlayTitle { font-size: 15px; font-weight: 700; color: #123; margin-bottom: 4px; }
            QLabel#overlayBody  { font-size: 14px; color: #123; }
            QLabel#overlayHint  { color: #567; font-size: 12px; margin-top: 8px; }

            /* Optional state tint */
            QWidget[state="correct"] QFrame#overlayCard { background: #9FE69F; }
            QWidget[state="wrong"]   QFrame#overlayCard { background: #FF8E8E; }
        """)

        # Root layout fills parent; centers the card automatically
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setAlignment(Qt.AlignCenter)
        self.setObjectName("OverlayRoot")

        self.card = QFrame(self)
        self.card.setObjectName("overlayCard")
        root.addWidget(self.card, 0, Qt.AlignCenter)

        box = QVBoxLayout(self.card)
        box.setContentsMargins(16, 14, 16, 14)  # compact padding
        box.setSpacing(6)
        box.setAlignment(Qt.AlignCenter)

        self.title = QLabel("", self); self.title.setObjectName("overlayTitle")
        self.body  = QLabel("", self); self.body.setObjectName("overlayBody"); self.body.setWordWrap(True)
        self.hint  = QLabel("Press any key or click to continue", self); self.hint.setObjectName("overlayHint")

        box.addWidget(self.title, 0, Qt.AlignHCenter)
        box.addWidget(self.body,  0, Qt.AlignHCenter)
        box.addWidget(self.hint,  0, Qt.AlignHCenter)

        # Optional shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24); shadow.setOffset(0, 6); shadow.setColor(QColor(0, 0, 0, 70))
        self.card.setGraphicsEffect(shadow)

        self._on_close = None

    def show_message(self, title: str, text: str, on_close=None, state: str | None = None):
        """Show the overlay without any auto-close. Dismiss via click or key."""
        self._on_close = on_close
        self.title.setText(title)
        self.body.setText(text)

        # Apply (or clear) state tint
        self.setProperty("state", state or "")
        self.style().unpolish(self); self.style().polish(self)

        # Make overlay cover the parent, then show
        parent = self.parentWidget()
        if parent:
            self.setGeometry(0, 0, parent.width(), parent.height())

        # NEW: widen the card up to 90% of the window, capped at 560px (tweak to taste)
        max_card_w = min(int(parent.width() * 0.90), 560)
        self.card.setMaximumWidth(max_card_w)

        # Make the QLabel wrap using the same width minus card padding (16+16)
        self.body.setFixedWidth(max_card_w - 32)

        # If you want to let it grow taller naturally:
        self.body.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.show()
        self.raise_()
        self.setFocus(Qt.ActiveWindowFocusReason)

    def _finish(self):
        self.hide()
        cb = self._on_close
        self._on_close = None
        if cb:
            cb()

    # Dismiss on any click or key
    def mousePressEvent(self, _): self._finish()
    def keyPressEvent(self,   _): self._finish()

    # Keep overlay stretched to parent when resized
    def resizeEvent(self, _ev):
        parent = self.parentWidget()
        if parent and self.isVisible():
            self.setGeometry(0, 0, parent.width(), parent.height())