from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QSequentialAnimationGroup, QAbstractAnimation


class FlashcardWidget(QWidget):
    """
    A single flashcard containing a question on the front
    and an answer on the back. Supports flipping with a width
    shrink/expand animation for a clean card-flip effect.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_flipped = False  # False = front/question shown

        self._build_ui()
        self._configure_animation()

    # ======================================================================
    # UI BUILDING
    # ======================================================================

    def _build_ui(self):
        """Creates and arranges all visual components."""

        # Outer layout (centers the flashcard widget)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Flashcard container
        self.face = QWidget()
        self.face.setObjectName("Flashcard")
        self.face.setFixedSize(300, 240)

        outer.addWidget(self.face, alignment=Qt.AlignHCenter)

        # Inside-card layout
        inner = QVBoxLayout(self.face)
        inner.setContentsMargins(20, 20, 20, 20)
        inner.setSpacing(10)

        # Title ("Question" / "Answer")
        self.title_label = QLabel("Question")
        self.title_label.setObjectName("FlashTitle")
        self.title_label.setAlignment(Qt.AlignCenter)
        inner.addWidget(self.title_label)

        # Main text areas
        self.front_label = self._create_text_label()
        self.back_label = self._create_text_label()
        self.back_label.hide()   # Start on the question side

        inner.addWidget(self.front_label)
        inner.addWidget(self.back_label)

        # Push hint to bottom
        inner.addStretch()

        # Hint text ("Tap the card ...")
        self.hint_label = QLabel("Tap the card to reveal the answer")
        self.hint_label.setObjectName("FlashHint")
        self.hint_label.setAlignment(Qt.AlignCenter)
        inner.addWidget(self.hint_label)

        # Enable clicking the card to flip it
        self.face.mousePressEvent = self.flip

    def _create_text_label(self):
        """Creates a centered, word-wrapped label for card text."""
        label = QLabel()
        label.setObjectName("FlashcardText")
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        return label

    # ======================================================================
    # ANIMATION SETUP
    # ======================================================================

    def _configure_animation(self):
        """Creates the shrink → swap → expand flip animation."""

        self.shrink = QPropertyAnimation(self.face, b"maximumWidth", self)
        self.expand = QPropertyAnimation(self.face, b"maximumWidth", self)

        self.anim_group = QSequentialAnimationGroup(self)
        self.anim_group.addAnimation(self.shrink)
        self.anim_group.addAnimation(self.expand)

        # Swap content at the midpoint of the animation
        self.shrink.finished.connect(self._swap_side)

    # ======================================================================
    # PUBLIC SETTERS
    # ======================================================================

    def set_front_text(self, text: str):
        """Updates the front (question) text."""
        self.front_label.setText(text)

    def set_back_text(self, text: str):
        """Updates the back (answer) text."""
        self.back_label.setText(text)

    def show_front(self):
        """Switches card to question side."""
        self.front_label.show()
        self.back_label.hide()
        self.is_flipped = False
        self.title_label.setText("Question")
        self.hint_label.setText("Tap the card to reveal the answer")

    def show_back(self):
        """Switches card to answer side."""
        self.front_label.hide()
        self.back_label.show()
        self.is_flipped = True
        self.title_label.setText("Answer")
        self.hint_label.setText("Tap to go back")

    # ======================================================================
    # FLIP LOGIC
    # ======================================================================

    def flip(self, event=None):
        """
        Starts the flip animation if no animation is already running.
        Shrinks width to zero, swaps side, then expands back.
        """

        if self.anim_group.state() != QAbstractAnimation.Stopped:
            return  # Ignore taps during animation

        full_width = max(self.face.width(), 300)

        # Shrink phase
        self.shrink.setDuration(150)
        self.shrink.setStartValue(full_width)
        self.shrink.setEndValue(0)

        # Expand phase
        self.expand.setDuration(150)
        self.expand.setStartValue(0)
        self.expand.setEndValue(full_width)

        self.anim_group.start()

    def _swap_side(self):
        """Switches text in the middle of the flip animation."""
        if self.is_flipped:
            self.show_front()
        else:
            self.show_back()