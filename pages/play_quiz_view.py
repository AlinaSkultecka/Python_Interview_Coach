from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from data.question_generator import generate_quiz_question

class PlayQuizView(QWidget):
    def __init__(self, main_menu):
        super().__init__()
        self.main_menu = main_menu
        self.setWindowTitle("Play Quiz")
        self.setFixedSize(360, 640)

        self.current_question = None

        self.layout = QVBoxLayout()
        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        self.option_buttons = []
        for _ in range(4):   # 4 options per question
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
        q = generate_quiz_question()  # Always get a new one!
        self.current_question = q
        self.question_label.setText(q.question)
        for i, option in enumerate(q.options):
            self.option_buttons[i].setText(option)
            self.option_buttons[i].setEnabled(True)

    def check_answer(self):
        sender = self.sender()
        selected = sender.text()
        selected_letter = selected[0].lower()
        q = self.current_question
        if q.is_correct(selected_letter):
            QMessageBox.information(self, "Correct!", "Good job!")
        else:
            QMessageBox.warning(self, "Incorrect", f"Correct answer: {q.correct}. {q.explanation}")

        self.show_question()

    def return_to_menu(self):
        self.main_menu.show()
        self.close()