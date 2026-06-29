# Console Quiz Application

A Python-based, terminal-based Quiz Application featuring OOP architecture, random/difficulty-filtered question selections, a native Windows input countdown timer, persistent JSON storage, metrics tracking, and a Top 10 Leaderboard.

## Project Structure

```text
quiz_app/
├── main.py             # Entry point, controls the CLI menu structure and user input flows.
├── quiz.py             # OOP core containing Question, User, and Quiz classes.
├── score_manager.py    # Manages loading, appending, and computing score metrics & leaderboard.
├── utils.py            # Utility functions including screen clear, options validation, and timed inputs.
├── questions.json      # JSON file loaded with pre-configured multiple-choice questions.
└── scores.json         # JSON database storing user attempt history.
```

---

## Features

1. **Start Quiz**:
   - Asks for user's name.
   - Choose difficulty level (Easy, Medium, Hard, or Mixed).
   - Toggle randomized questions.
   - Toggle a **30-second per-question countdown timer** (shows remaining time in the console title bar on Windows!).
   - Continuous timer: entering invalid answers recalculates remaining time instead of resetting it.
2. **View Previous Scores**:
   - Prints history of all quiz attempts.
   - Computes and displays overall stats (Total Attempts, Highest Score, Average Score).
   - Generates a **Top 10 Leaderboard** sorted by score percentages.
3. **Add New Questions (Admin)**:
   - Interactive prompt to add questions.
   - Full input validations for fields (non-empty question/options, valid correct answers A-D, valid difficulties).
   - Automatically saves and appends to `questions.json`.
4. **Input Validation & Error Handling**:
   - Robust JSON decoding error handling (for corrupt databases).
   - Normalizes input cases.
   - Handles `KeyboardInterrupt` (Ctrl+C) gracefully to clear terminals and exit safely.

---

## Requirements

- Python 3.6 or higher.
- standard library only (no third-party pip installations required!).

---

## How to Run the Project

1. Open a terminal (PowerShell or Command Prompt on Windows, Terminal on macOS/Linux).
2. Navigate to the project directory:
   ```bash
   cd Z:\Project\Quiz App\scratch\quiz_app
   ```
3. Run the application:
   ```bash
   python main.py
   ```

---

## How to Test and Verify

### 1. Taking a Quiz
Choose Option **1** from the Main Menu. Enter your name, select difficulty, and choose whether to enable the timer. Answer questions by typing `A`, `B`, `C`, or `D`. If you let the timer expire, it will mark it as missed and move to the next question.

### 2. Viewing Statistics & Leaderboard
Choose Option **2** from the Main Menu. If no attempts have been made yet, it will prompt you to take a quiz first. Otherwise, it will print a formatted table of all attempts, calculate average and highest scores, and display the Top 10 Leaderboard.

### 3. Adding New Questions
Choose Option **3** from the Main Menu. Fill in the question, option details, correct answer letter, and difficulty. When finished, it will save it. Take a quiz again to verify the new question shows up.

### 4. Exit
Exits the program saying: Thank you for using the Console Quiz Application. Goodbye!