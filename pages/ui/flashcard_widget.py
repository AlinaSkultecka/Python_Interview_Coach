from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QSequentialAnimationGroup, QAbstractAnimation


class FlashcardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.is_flipped = False  # False = front/question

        # --- Outer layout (centers card) ---
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # --- White flashcard face ---
        self.face = QWidget()
        self.face.setObjectName("Flashcard")
        self.face.setFixedSize(300, 240)      # ← bigger card
        self.face.setMinimumWidth(300)

        outer.addWidget(self.face, alignment=Qt.AlignHCenter)

        # --- Inside flashcard layout ---
        inner = QVBoxLayout(self.face)
        inner.setContentsMargins(20, 20, 20, 20)
        inner.setSpacing(10)

        # TITLE LABEL (Question 1 / Answer)
        self.title_label = QLabel("Question")
        self.title_label.setObjectName("FlashTitle")
        self.title_label.setAlignment(Qt.AlignCenter)

        inner.addWidget(self.title_label)

        # CENTER TEXT BLOCK (VERTICALLY)
        center_block = QVBoxLayout()
        center_block.setAlignment(Qt.AlignCenter)

        # FRONT (question)
        self.front_label = QLabel()
        self.front_label.setObjectName("FlashcardText")
        self.front_label.setAlignment(Qt.AlignCenter)
        self.front_label.setWordWrap(True)

        # BACK (answer)
        self.back_label = QLabel()
        self.back_label.setObjectName("FlashcardText")
        self.back_label.setAlignment(Qt.AlignCenter)
        self.back_label.setWordWrap(True)
        self.back_label.hide()

        # --- Add both labels ---
        inner.addWidget(self.front_label)
        inner.addWidget(self.back_label)

        inner.addLayout(center_block)

        # --- Push hint to bottom ---
        inner.addStretch()

        # BOTTOM HINT (inside card)
        self.hint_label = QLabel("Tap the card to reveal the answer")
        self.hint_label.setObjectName("FlashHint")
        self.hint_label.setAlignment(Qt.AlignCenter)

        inner.addWidget(self.hint_label)

        # Click to flip
        self.face.mousePressEvent = self.flip

        # --- Flip animation (width shrink + expand) ---
        self.shrink = QPropertyAnimation(self.face, b"maximumWidth", self)
        self.expand = QPropertyAnimation(self.face, b"maximumWidth", self)

        self.anim_group = QSequentialAnimationGroup(self)
        self.anim_group.addAnimation(self.shrink)
        self.anim_group.addAnimation(self.expand)

        self.shrink.finished.connect(self._swap_side)

    # ---------------------------------------
    # SETTERS
    # ---------------------------------------
    def set_front_text(self, text):
        self.front_label.setText(text)

    def set_back_text(self, text):
        self.back_label.setText(text)

    def show_front(self):
        self.front_label.show()
        self.back_label.hide()
        self.is_flipped = False
        self.hint_label.setText("Tap the card to reveal the answer")

    def show_back(self):
        self.front_label.hide()
        self.back_label.show()
        self.is_flipped = True
        self.hint_label.setText("Tap the card to go back")

    # ---------------------------------------
    # FLIP ANIMATION
    # ---------------------------------------
    def flip(self, event=None):

        if self.anim_group.state() != QAbstractAnimation.Stopped:
            return

        full_width = self.face.width()
        if full_width <= 0:
            full_width = 300

        # shrink to 0
        self.shrink.setDuration(150)
        self.shrink.setStartValue(full_width)
        self.shrink.setEndValue(0)

        # expand back to full width
        self.expand.setDuration(150)
        self.expand.setStartValue(0)
        self.expand.setEndValue(full_width)

        self.anim_group.start()

    # ---------------------------------------
    # TEXT SWAP IN THE MIDDLE OF FLIP
    # ---------------------------------------
    def _swap_side(self):
        if not self.is_flipped:
            self.show_back()
            self.title_label.setText("Answer")
            self.hint_label.setText("Tap to go back")
        else:
            self.show_front()
            self.title_label.setText("Question")
            self.hint_label.setText("Tap the card to reveal the answer")