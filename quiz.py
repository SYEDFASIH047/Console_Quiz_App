import json
import random
import time
from datetime import datetime
from utils import clear_screen, get_timed_input

class Question:
    def __init__(self, q_id, question, options, correct_answer, difficulty):
        self.id = q_id
        self.question = question
        self.options = options  # dictionary: {"A": "...", "B": "...", ...}
        self.correct_answer = correct_answer.strip().upper()
        self.difficulty = difficulty.strip().capitalize()

    def check_answer(self, user_answer):
        return user_answer.strip().upper() == self.correct_answer

    @classmethod        # Built-in Python function\method
    def from_dict(cls, data):

        """Can be called directly from the class without creating an object first."""
        return cls(
            q_id=data.get("id"),
            question=data.get("question"),
            options=data.get("options"),
            correct_answer=data.get("correct_answer"),
            difficulty=data.get("difficulty", "Medium")
        )

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "difficulty": self.difficulty
        }


class User:
    def __init__(self, name):
        self.name = name.strip()


class Quiz:
    def __init__(self, questions_file="questions.json", difficulty=None, randomize=True, use_timer=True):
        self.questions_file = questions_file
        self.difficulty = difficulty  # "Easy", "Medium", "Hard", or None
        self.randomize = randomize
        self.use_timer = use_timer
        self.time_limit = 30  #30 seconds per question
        self.questions = [10]
        self.user = None
        self.score = 0
        self.results = {}

    def load_questions(self):
        """Loads questions from JSON and filters by difficulty if set."""

        try:
            with open(self.questions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            all_questions = [Question.from_dict(q) for q in data]
            
            if self.difficulty:
                self.questions = [q for q in all_questions if q.difficulty.upper() == self.difficulty.upper()]
            else:
                self.questions = all_questions

            if not self.questions:
                raise ValueError("No questions found matching criteria.")

            if self.randomize:
                random.shuffle(self.questions)

        except FileNotFoundError:
            print(f"Error: The file {self.questions_file} was not found.")
            raise
        except json.JSONDecodeError:
            print(f"Error: The file {self.questions_file} contains invalid JSON.")
            raise
        except Exception as e:
            print(f"Error loading questions: {e}")
            raise

    def start(self, user_name):
        """Starts and runs the quiz session."""

        self.user = User(user_name)
        self.score = 0
        self.results = {
            "name": self.user.name,
            "total_questions": len(self.questions),
            "correct_answers": 0,
            "wrong_answers": 0,
            "percentage": 0.0,
            "status": "FAIL",
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        print(f"\nWelcome, {self.user.name}! The quiz is starting now.")
        print(f"Total Questions: {len(self.questions)}")
        if self.use_timer:
            print(f"Timer Enabled: You have {self.time_limit} seconds per question.")
        print("-" * 50)
        time.sleep(1.5)

        for i, q in enumerate(self.questions, 1):
            clear_screen()
            print(f"\nQuestion {i} of {len(self.questions)} [Difficulty: {q.difficulty}]")
            print("=" * 50)
            print(q.question)
            print("-" * 50)
            for opt_key, opt_val in sorted(q.options.items()):
                print(f"  {opt_key}. {opt_val}")
            print("-" * 50)

            # Answer input with validation and persistent timer calculation

            user_answer = ""
            start_time = time.time()
            
            while True:
                if self.use_timer:
                    elapsed = time.time() - start_time
                    remaining = self.time_limit - elapsed
                    if remaining <= 0:
                        print("\n[Time's up!]")
                        user_answer = ""
                        break
                    
                    ans = get_timed_input("Enter your answer (A/B/C/D): ", timeout=remaining)

                    if ans == "": # Timeout occurred inside get_timed_input
                        user_answer = ""
                        break
                else:
                    ans = input("Enter your answer (A/B/C/D): ").strip()

                ans_upper = ans.upper()
                if ans_upper in ('A', 'B', 'C', 'D'):
                    user_answer = ans_upper
                    break
                else:
                    print("Invalid choice! Please select A, B, C, or D.")

            # Evaluate answer after timeout

            if user_answer == "":
                print(f"No answer submitted. Correct answer was: {q.correct_answer}")
                self.results["wrong_answers"] += 1
            elif q.check_answer(user_answer):
                print("Correct!")
                self.score += 1
                self.results["correct_answers"] += 1
            else:
                print(f"Wrong answer. Correct answer was: {q.correct_answer}")
                self.results["wrong_answers"] += 1

            time.sleep(1.5)

        # Finalize results

        self.results["score"] = self.score
        if len(self.questions) > 0:
            pct = (self.score / len(self.questions)) * 100
            self.results["percentage"] = round(pct, 2)
        else:
            self.results["percentage"] = 0.0

        if self.results["percentage"] >= 60.0:
            self.results["status"] = "PASS"
        else:
            self.results["status"] = "FAIL"

    def display_results(self):
        """Displays the formatted score sheet to the user."""

        clear_screen()
        print("\n" + "=" * 50)
        print("                 QUIZ COMPLETED")
        print("=" * 50)
        print(f"  Name:             {self.results['name']}")
        print(f"  Total Questions:  {self.results['total_questions']}")
        print(f"  Correct Answers:  {self.results['correct_answers']}")
        print(f"  Wrong Answers:    {self.results['wrong_answers']}")
        print(f"  Score:            {self.results['score']}/{self.results['total_questions']}")
        print(f"  Percentage:       {self.results['percentage']}%")
        
        status_color = "[PASS]" if self.results['status'] == "PASS" else "[FAIL]"
        print(f"  Status:           {status_color}")
        print("=" * 50 + "\n")
