from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton
from PyQt5.QtCore import QTimer


class Quiz(QWidget):
    def __init__(self, questions):
        super().__init__()
        self.questions = questions
        self.total_questions = len(questions)
        self.current_question = 0
        self.score = 0
        self.score_label = QLabel()
        self.question_label = QLabel()
        self.timer_label = QLabel()
        self.option_1 = QRadioButton()
        self.option_2 = QRadioButton()
        self.option_3 = QRadioButton()
        self.option_4 = QRadioButton()

        self.previous_button = QPushButton('Previous', self)
        self.submit_button = QPushButton('Submit')

        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # 1 second
        self.timer.timeout.connect(self.update_timer)
        self.total_time = 600
        self.remaining_time = 600
        self.question_scores = {i: 0 for i in range(self.total_questions)}
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('Multiple Choice Quiz')
        layout = QVBoxLayout()
        layout.addWidget(self.question_label)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.option_1)
        layout.addWidget(self.option_2)
        layout.addWidget(self.option_3)
        layout.addWidget(self.option_4)
        layout.addWidget(self.previous_button)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
        self.submit_button.clicked.connect(self.submitAnswer)
        self.previous_button.clicked.connect(self.previous_button_clicked)
        self.showQuestion()

    def finishQuiz(self):
        self.timer.stop()
        self.displayScore()
    def showQuestion(self):
        if self.current_question >= self.total_questions:
            self.finishQuiz()
        else:
            question = self.questions[self.current_question]
            self.question_label.setText(question['question'])
            self.option_1.setText(question['options'][0])
            self.option_2.setText(question['options'][1])
            self.option_3.setText(question['options'][2])
            self.option_4.setText(question['options'][3])
            self.option_1.setChecked(False)
            self.option_2.setChecked(False)
            self.option_3.setChecked(False)
            self.option_4.setChecked(False)

            if self.question_scores[self.current_question] > 0:
                self.score_label.setText(
                    f"Score: {self.score - self.question_scores[self.current_question]} / {self.total_questions * 10}")
            else:
                self.score_label.setText(f"Score: {self.score} / {self.total_questions * 10}")

            if self.current_question >= self.total_questions - 1:
                self.submit_button.setText('Finish')
            else:
                self.submit_button.setText('Submit')

            if self.current_question == 0:
                self.previous_button.setEnabled(False)
            else:
                self.previous_button.setEnabled(True)

            if self.current_question == self.total_questions:
                self.previous_button.hide()
            else:
                self.previous_button.show()

            self.submit_button.setEnabled(self.current_question < self.total_questions - 1)
            self.previous_button.setEnabled(self.current_question > 0)
            self.previous_button.setEnabled(True)
            self.submit_button.setEnabled(True)
            self.timer.start()
            self.update_timer()

    def previous_button_clicked(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.showQuestion()

    def update_timer(self):
        self.remaining_time -= 1
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timer_label.setText(f"Time Left: {minutes:02d}:{seconds:02d}")

        if self.remaining_time == 0:
            self.timer.stop()
            self.displayScore()
        elif self.current_question == self.total_questions - 1:
            self.timer.stop()

    def submitAnswer(self):
        question = self.questions[self.current_question]
        selected_option = None
        if self.option_1.isChecked():
            selected_option = self.option_1.text()
        elif self.option_2.isChecked():
            selected_option = self.option_2.text()
        elif self.option_3.isChecked():
            selected_option = self.option_3.text()
        elif self.option_4.isChecked():
            selected_option = self.option_4.text()

        if self.current_question in self.question_scores:
            previous_score = self.question_scores[self.current_question]
        else:
            previous_score = 0

        if selected_option == question['answer']:
            self.score += 10 - previous_score
            self.question_scores[self.current_question] = 10
        else:
            self.question_scores[self.current_question] = 0

        if self.current_question == len(self.questions) - 1:
            self.displayScore()
        else:
            self.current_question += 1
            self.showQuestion()

    def displayScore(self):
        total_score = 0
        num_correct = 0
        num_incorrect = 0
        incorrect_questions = []

        for i in range(self.total_questions):
            if self.question_scores[i]:
                total_score += 10
                num_correct += 1
            else:
                num_incorrect += 1
                incorrect_questions.append(i + 1)
        if num_incorrect == 0:
            incorrect_questions.append(+ 0)
        gpa = None
        percentage = None
        if num_correct > 0:
            percentage = (num_correct / self.total_questions) * 100
            if percentage >= 90:
                gpa = 'A'
            elif percentage >= 80:
                gpa = 'B'
            elif percentage >= 70:
                gpa = 'C'
            elif percentage >= 60:
                gpa = 'D'
            else:
                gpa = 'F'
        minutes2 = (self.total_time-self.remaining_time)//60
        seconds2 = (self.total_time-self.remaining_time) % 60
        result = f"Number of Correct Answers: {num_correct}\n"\
                 f"Number of Incorrect Answers: {num_incorrect}\n"\
                 f"Total Score: {total_score}\n"\
                 f"GPA: {gpa}\n"\
                 f"Percentage: {percentage}%\n"\
                 f"Incorrect Questions: {incorrect_questions}\n" \
                 f"Time Spent: {minutes2:02d}:{seconds2:02d}"
        self.question_label.setText(result)
        self.option_1.hide()
        self.option_2.hide()
        self.option_3.hide()
        self.option_4.hide()
        self.submit_button.hide()
        self.previous_button.hide()


if __name__ == '__main__':
    app = QApplication([])
    questions = [
        {
            'question': 'Who was the father of computer?',
            'options': ['Charlie Babbage', 'Dennis Richie', 'Charles Babbage', 'Ken Thompson'],
            'answer': 'Charles Babbage'
        },
        {
            'question': 'What is the full form of CPU?',
            'options': ['Central Process Unit', 'Central Processing Unit', 'Central Programming Unit', 'Central Unit'],
            'answer': 'Central Processing Unit'
        },
        {
            'question': 'What is the full form of CU?',
            'options': ['Compound Unit', 'Communication Unit', 'Computer Unit', 'Control Unit'],
            'answer': 'Control Unit'
        },
        {
            'question': 'What is the full form of ALU?',
            'options': ['Arithmetic Logic Unit', 'Arithmetic Local Unit', 'Advance Logical Unit', 'None of these'],
            'answer': 'Arithmetic Logic Unit'
        },
        {
            'question': 'What is the full form of MU?',
            'options': ['Management Unit', 'Masked Unit', 'Main Unit', 'Memory Unit'],
            'answer': 'Memory Unit'
        },
        {
            'question': 'What is the full form of EEPROM?',
            'options': ['Electrically Erasable Read Access Memory', 'Electrically Erasable Read Only Memory', 'Ethical Electrically Read Only Memory', 'None of these'],
            'answer': 'Electrically Erasable Read Only Memory'
        },
        {
            'question': 'What is the full form of SDRAM?',
            'options': ['Special Dynamic Read Access Memory', 'Synchronous Dynamic Read Access Memory', 'Special Dynamic Random Access Memory', 'Synchronous Dynamic Random Access Memory'],
            'answer': 'Synchronous Dynamic Random Access Memory'
        },
        {
            'question': 'Which is not a correct type of a computer?',
            'options': ['Mini Frame Computer', 'Super Computer', 'Workstations', 'Personal Computer'],
            'answer': 'Mini Frame Computer'
        },
        {
            'question': 'Which electronics component is used in first generation computers?',
            'options': ['Transistors', 'ULSI Chips', 'Vacuum Tubes', 'LSI Chips'],
            'answer': 'Vacuum Tubes'
        },
        {
            'question': 'Which part of the computer is considered as Brain of the Computer?',
            'options': ['Random Access Memory', 'Central Process Unit', 'Read Only Memory', 'Hard Disk'],
            'answer': 'Central Process Unit'
        }
    ]
    quiz = Quiz(questions)
    quiz.show()
    app.exec()


#3,2,4,1,4,2,4,1,3,2
