from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from data.question_generator import generate_quiz_question

class PlayQuizView(QWidget):
    def __init__(self, main_menu):
        super().__init__()
        self.main_menu = main_menu
        self.setWindowTitle("Play Quiz")
        self.setFixedSize(360, 640)

        # --- Instead of a list, just draw new questions as needed
        self.questions = [generate_quiz_question() for _ in range(2)]  # e.g., 2 random questions
        self.current_index = 0

        self.layout = QVBoxLayout()
        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        self.option_buttons = []
        for _ in range(3):
            btn = QPushButton()
            btn.clicked.connect(self.check_answer)
            self.option_buttons.append(btn)
            self.layout.addWidget(btn)

        self.btn_back = QPushButton("Return to Menu")
        self.btn_back.clicked.connect(self.return_to_menu)
        self.layout.addWidget(self.btn_back)

        self.setLayout(self.layout)
        self.show_question()

    def show_question(self):
        q = self.questions[self.current_index]
        self.question_label.setText(q["question"])
        for i, option in enumerate(q["options"]):
            self.option_buttons[i].setText(option)
            self.option_buttons[i].setEnabled(True)

    def check_answer(self):
        sender = self.sender()
        selected = sender.text()
        # Extract the letter ("A.", "B.", "C.") if needed
        selected_letter = selected[0]
        correct_letter = self.questions[self.current_index]["correct"]

        if selected_letter == correct_letter:
            QMessageBox.information(self, "Correct!", "Good job!")
        else:
            QMessageBox.warning(self, "Incorrect", f"Correct answer: {correct_letter}. {self.questions[self.current_index]['explanation']}")

        # Move to next question or finish
        self.current_index += 1
        if self.current_index < len(self.questions):
            self.show_question()
        else:
            QMessageBox.information(self, "Quiz Finished", "You completed the quiz!")
            self.return_to_menu()

    def return_to_menu(self):
        self.main_menu.show()
        self.close()