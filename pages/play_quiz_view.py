from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer

from data.question_generator import generate_quiz_question
from pages.ui.feedback_overlay import FeedbackOverlay
from pages.ui.answer_button import AnswerButton

class PlayQuizView(QWidget):
    def __init__(self, main_menu):
        super().__init__()
        self.main_menu = main_menu
        self.setWindowTitle("Play Quiz")
        self.setFixedSize(360, 640)

        # --- State ---
        self.correct_count = 0
        self.total_count = 0
        self.current_question = None
        self.question_counter = 0

        # --- Root layout ---
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)
        self.setObjectName("Root")

        self.overlay = FeedbackOverlay(self)

        # --- Styles ---
        self.setStyleSheet("""
            QWidget#Root {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #5ea3ff, stop:1 #4667ff);
                border-radius: 20px;
            }
            QLabel#Score { color: white; font-weight: bold; font-size: 16px; }
            QLabel#Tiny  { color: rgba(255,255,255,0.9); font-size: 16px; }
            QLabel#Question { color: white; font-size: 22px; font-weight: 700; }

            QPushButton#BackBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #fff7b1, stop:1 #ffd84d);
                color: #3a3500;
                border: none;
                border-radius: 20px;
                padding: 10px 22px;
                font-size: 16px;
                font-weight: 600;
                min-width: 100px;
                min-height: 20px;
                box-shadow: 0 2px 8px rgba(60,60,0,0.07);
            }
            QPushButton#BackBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ffe066, stop:1 #ffd84d);
                color: #2d2d05;
            }
        """)

        # --- TOP BAR (rounded "Return to Menu" button) ---
        top = QHBoxLayout()
        top.setSpacing(8)

        self.btn_back = QPushButton("Return to Menu")
        self.btn_back.setObjectName("BackBtn")
        self.btn_back.clicked.connect(self.return_to_menu)
        # Optionally make it visually wider:
        self.btn_back.setMinimumWidth(50)
        self.btn_back.setCursor(Qt.PointingHandCursor)

        self.score_label = QLabel(self._score_text())
        self.score_label.setObjectName("Score")
        top.addWidget(self.btn_back)
        top.addStretch(1)
        top.addWidget(self.score_label)
        root.addLayout(top)

        # --- Question meta + text ---
        meta = QVBoxLayout(); meta.setSpacing(6)
        self.meta_label = QLabel("")      # e.g., "question 23"
        self.meta_label.setObjectName("Tiny")
        self.question_label = QLabel()
        self.question_label.setObjectName("Question")
        self.question_label.setWordWrap(True)
        self.question_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        meta.addWidget(self.meta_label)
        meta.addWidget(self.question_label)
        root.addLayout(meta)

        root.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # --- Answer buttons (always 4) pinned at bottom ---
        self.option_buttons = []
        self.answers_box = QVBoxLayout()
        self.answers_box.setSpacing(8)

        for i in range(4):
            btn = AnswerButton()
            btn.clicked.connect(lambda idx=i: self.check_answer(idx))
            self.answers_box.addWidget(btn)
            self.option_buttons.append(btn)

        root.addLayout(self.answers_box)

        self.show_question()

    # ---------- Helpers ----------
    def _score_text(self):
        return f"Score: {self.correct_count}/{self.total_count}"

    def _update_top(self):
        self.score_label.setText(self._score_text())

    def _advance_after_correct(self):
        for btn in self.option_buttons:
            if hasattr(btn, "setState"):
                btn.setState(None)
            btn.setSelected(False)
            btn.setEnabled(True)
        self.show_question()

    # ---------- Game Flow ----------
    def show_question(self):
        self.question_counter += 1
        self._update_top()

        q = generate_quiz_question()
        self.current_question = q

        self.meta_label.setText(f"question {self.question_counter}")
        self.question_label.setText(q.question)

        assert len(q.options) == 4
        for i, btn in enumerate(self.option_buttons):
            btn.setText(q.options[i])
            btn.setSelected(False)
            if hasattr(btn, "setState"):
                btn.setState(None)
            btn.setEnabled(True)

    def check_answer(self, idx):
        if not self.current_question:
            return

        # visually select the clicked option
        for i, btn in enumerate(self.option_buttons):
            btn.setSelected(i == idx)

        q = self.current_question
        letter = "abcd"[idx]

        self.total_count += 1
        is_ok = hasattr(q, "is_correct") and q.is_correct(letter)

        # disable all buttons while we show feedback
        for btn in self.option_buttons:
            btn.setEnabled(False)

        if is_ok:
            self.correct_count += 1
            self._update_top()

            # flash the clicked button green briefly, then advance
            if hasattr(self.option_buttons[idx], "setState"):
                self.option_buttons[idx].setState("correct")

            QTimer.singleShot(900, self._advance_after_correct)
            return

        # Wrong answer path: mark wrong + show overlay (with explanation)
        self._update_top()

        # mark clicked red
        if hasattr(self.option_buttons[idx], "setState"):
            self.option_buttons[idx].setState("wrong")

        # mark the correct one green, if we know it
        try:
            correct_idx = "abcd".index(q.correct.lower())
            if hasattr(self.option_buttons[correct_idx], "setState"):
                self.option_buttons[correct_idx].setState("correct")
        except Exception:
            pass

        msg = f"Correct answer: {getattr(q, 'correct', '?')}.\n{getattr(q, 'explanation', '')}"
        # overlay only on wrong; advance to next question when overlay closes
        self.overlay.show_message("Incorrect", msg, on_close=self.show_question, state="wrong")

    def return_to_menu(self):
        self.main_menu.show()
        self.close()