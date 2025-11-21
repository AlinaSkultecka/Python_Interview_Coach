from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, QEvent

from data.question_generator import generate_quiz_question
from pages.ui.feedback_overlay import FeedbackOverlay
from pages.ui.answer_button import AnswerButton


class PlayQuizView(QWidget):
    """
    Quiz gameplay screen.
    Handles question display, answer checking, scoring,
    and user interaction flow.
    """

    def __init__(self, main_menu):
        super().__init__()
        self.main_menu = main_menu

        # Window setup
        self.setWindowTitle("Play Quiz")
        self.setFixedSize(360, 640)

        # --- Quiz State ---
        self.correct_count = 0
        self.total_count = 0
        self.current_question = None
        self.question_counter = 0

        # Used when a correct answer is selected
        # and the system waits for key/click to continue
        self.waiting_for_next = False
        self.installEventFilter(self)

        # --- UI Setup ---
        self._build_ui()
        self._apply_styles()

        # Load first question
        self.show_question()

    # ======================================================================
    # UI BUILDING
    # ======================================================================

    def _build_ui(self):
        """Creates and arranges all UI elements."""
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # --- Top bar -------------------------------------------------------
        top_row = QWidget()
        top_row.setObjectName("TopRow")

        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(16, 12, 16, 12)

        self.btn_back = QPushButton("Return to Menu")
        self.btn_back.setObjectName("BackBtn")
        self.btn_back.clicked.connect(self.return_to_menu)
        self.btn_back.setCursor(Qt.PointingHandCursor)

        self.score_label = QLabel(self._score_text())
        self.score_label.setObjectName("Score")

        top_layout.addWidget(self.btn_back)
        top_layout.addStretch()
        top_layout.addWidget(self.score_label)

        outer.addWidget(top_row)

        # --- Gradient Content Area -----------------------------------------
        content = QWidget()
        content.setObjectName("Root")

        root = QVBoxLayout(content)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(8)

        outer.addWidget(content)

        # --- Feedback overlay (wrong answers) ------------------------------
        self.overlay = FeedbackOverlay(self)

        # --- Question metadata + text --------------------------------------
        meta = QVBoxLayout()
        meta.setSpacing(6)

        self.meta_label = QLabel("")
        self.meta_label.setObjectName("Tiny")

        self.question_label = QLabel()
        self.question_label.setObjectName("Question")
        self.question_label.setWordWrap(True)
        self.question_label.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding
        )

        meta.addWidget(self.meta_label)
        meta.addWidget(self.question_label)
        root.addLayout(meta)

        # --- Space before answer buttons -----------------------------------
        root.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # --- "Press any key" hint ------------------------------------------
        self.continue_label = QLabel("")
        self._style_continue_hint()
        self.continue_label.hide()

        root.addWidget(self.continue_label)

        # --- Answer buttons ------------------------------------------------
        self.option_buttons = []
        self.answers_box = QVBoxLayout()
        self.answers_box.setSpacing(8)

        for i in range(4):
            btn = AnswerButton()
            btn.clicked.connect(lambda index=i: self.check_answer(index))
            self.answers_box.addWidget(btn)
            self.option_buttons.append(btn)

        root.addLayout(self.answers_box)

    # ======================================================================
    # STYLING HELPERS
    # ======================================================================

    def _apply_styles(self):
        """Applies global stylesheet rules for UI aesthetics."""
        self.setStyleSheet("""
            QWidget#TopRow {
                background: white;
            }
            QWidget#Root {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #D959A8, stop:1 #D95968
                );
            }
            QLabel#Score {
                color: #333;
                font-weight: bold;
                font-size: 16px;
            }
            QLabel#Tiny  {
                color: rgba(255,255,255,0.9);
                font-size: 16px;
                font-weight: 700;
            }
            QLabel#Question {
                color: white;
                font-size: 18px;
                font-weight: 700;
            }
            QPushButton#BackBtn {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #fff7b1, stop:1 #ffd84d
                );
                color: #3a3500;
                border: none;
                border-radius: 18px;
                padding: 10px;
                font-size: 16px;
                font-weight: 600;
                box-shadow: 0 2px 8px rgba(60,60,0,0.07);
            }
            QPushButton#BackBtn:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ffe066, stop:1 #ffd84d
                );
            }
        """)

    def _style_continue_hint(self):
        """Styles the subtle 'press any key' label."""
        self.continue_label.setAlignment(Qt.AlignCenter)
        self.continue_label.setStyleSheet(
            "color: rgba(255,255,255,0.65); font-size: 13px; font-weight: 400;"
        )

    # ======================================================================
    # QUIZ HELPERS
    # ======================================================================

    def _score_text(self):
        return f"Score: {self.correct_count}/{self.total_count}"

    def _update_top(self):
        """Refreshes score display."""
        self.score_label.setText(self._score_text())

    def disable_all_buttons(self):
        """Prevents all answer buttons from being clicked."""
        for button in self.option_buttons:
            button.setEnabled(False)

    def _advance_after_correct(self):
        """Resets UI and loads the next question."""
        for btn in self.option_buttons:
            if hasattr(btn, "setState"):
                btn.setState(None)
            btn.setSelected(False)
            btn.setEnabled(True)

        self.show_question()

    # ======================================================================
    # MAIN GAME FLOW
    # ======================================================================

    def show_question(self):
        """Loads and displays a new quiz question."""
        self.question_counter += 1
        self._update_top()

        question = generate_quiz_question()
        self.current_question = question

        # Question metadata
        self.meta_label.setText(f"Question {self.question_counter}")

        # Capitalize first letter of question text
        text = question.question.strip()
        self.question_label.setText(text[0].upper() + text[1:] if text else text)

        # Update answer buttons
        for i, btn in enumerate(self.option_buttons):
            btn.setText(question.options[i])
            btn.setSelected(False)
            if hasattr(btn, "setState"):
                btn.setState(None)
            btn.setEnabled(True)

    def check_answer(self, selected_index):
        """Handles a button click and determines correctness."""
        if not self.current_question:
            return

        # Highlight selected button
        for i, btn in enumerate(self.option_buttons):
            btn.setSelected(i == selected_index)

        question = self.current_question
        selected_letter = "abcd"[selected_index]

        self.total_count += 1
        is_correct = question.is_correct(selected_letter)

        # Lock answer buttons
        self.disable_all_buttons()

        if is_correct:
            # Mark answer as correct visually
            self.correct_count += 1
            self._update_top()

            if hasattr(self.option_buttons[selected_index], "setState"):
                self.option_buttons[selected_index].setState("correct")

            # Show hint + wait for user interaction
            self.continue_label.setText("Press any key to continue…")
            self.continue_label.show()

            self.waiting_for_next = True
            return

        # Wrong answer handling
        if hasattr(self.option_buttons[selected_index], "setState"):
            self.option_buttons[selected_index].setState("wrong")

        # Highlight correct choice
        try:
            correct_index = "abcd".index(question.correct.lower())
            if hasattr(self.option_buttons[correct_index], "setState"):
                self.option_buttons[correct_index].setState("correct")
        except Exception:
            pass

        # Show explanation overlay
        msg = f"Correct answer: {question.correct}.\n{question.explanation}"
        self.overlay.show_message("Incorrect", msg, on_close=self.show_question, state="wrong")

    # ======================================================================
    # NAVIGATION + EVENT HANDLING
    # ======================================================================

    def eventFilter(self, obj, event):
        """
        Captures mouse clicks or key presses when the quiz
        is waiting for the user to continue after a correct answer.
        """
        if self.waiting_for_next:
            if event.type() in (QEvent.MouseButtonPress, QEvent.KeyPress):
                self._continue_after_wait()
                return True

        return super().eventFilter(obj, event)

    def _continue_after_wait(self):
        """Clears hint and advances to next question."""
        self.waiting_for_next = False
        self.continue_label.hide()
        self._advance_after_correct()

    def return_to_menu(self):
        """Returns to the main menu."""
        self.main_menu.show()
        self.close()