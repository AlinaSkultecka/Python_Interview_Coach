# 🐍 Python Interview Coach

A modern desktop app to help you prepare for Python interviews using quizzes and flashcards!


## ✨ Features

### Quiz Mode
- Multiple-choice questions  
- Instant correctness feedback  
- Score tracking  
- Game-over summary + best-score comparison  
- Restart option

### Premade Flashcards 
- 20 curated Python concept flashcards  
- Smooth flip animation  
- Game-over screen  

### AI Flashcards (GPT-4.1 Mini)
- Enter any topic → receive AI-generated flashcards  
- Modern UI with animated “snake” border while generating  
- Uses your OpenAI key stored safely in `.env`

### Modern UI Components
- Gradient menu buttons  
- Animated answer cards  
- Flip-card widget  
- Clean mobile-style layout (360×640)  

## 🛠️ Tech Stack

- [Python 3](https://www.python.org/)
- [PySide6 (Qt for Python)](https://doc.qt.io/qtforpython/)
- [OpenAI GPT-4.1 Mini](https://platform.openai.com/docs/models/gpt-4.1-mini/)
- Qt Designer-style custom widgets
- JSON storage for quiz and flashcards data
- `.env` for your OPEN AI KEY  

### Image Credits

- Quiz icons by [Freepik - Flaticon](https://www.flaticon.com/free-icons/quiz)
- Flash cards icons by [manshagraphics - Flaticon](https://www.flaticon.com/free-icons/flash-cards)
- Quiz questions by [Python MCQ (Multiple Choice Questions)](https://www.sanfoundry.com/1000-python-questions-answers/)
- Flashcards #1 by [Python Interview Questions](https://www.w3schools.com/python/python_interview_questions.asp)
- Flashcards #2 by [Python Interview Questions](https://www.interviewbit.com/python-interview-questions/#list-vs-tuple)

## 📦 Installation
💡 Note: PyCharm is optional.
You only need Python to run this app.
```bash
1. Clone the repository
   git clone https://github.com/AlinaSkultecka/PythonInterviewCoach.git
   cd PythonInterviewCoach

2. Create a virtual environment (recommended) 
   /* Windows */
   python -m venv venv
   venv\Scripts\activate

   /* macOS / Linux */
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies
   pip install -r requirements.txt

4. Add your OpenAI API key (optional, required for AI flashcards)
   Create a .env file and add:
   OPENAI_API_KEY=your-openai-key-here

5. Run the application
   python main.py

6. (Optional) Update dependencies later
   pip install --upgrade -r requirements.txt
```

## 👩‍💻 Credits

- Design inspiration from modern mobile quiz apps.
- Created by Alina Skultecka (https://github.com/AlinaSkultecka).
