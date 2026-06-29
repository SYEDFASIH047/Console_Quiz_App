import os
import json
import sys
from quiz import Quiz
from score_manager import ScoreManager
from utils import clear_screen, get_valid_choice

def show_main_menu():
    """Displays the main menu options.""" # Display Main Menu

    clear_screen()
    print("\n" + "=" * 50)
    print("             CONSOLE QUIZ APPLICATION")
    print("=" * 50)
    print("  1. Start Quiz")
    print("  2. View Previous Scores & Leaderboard")
    print("  3. Add New Questions")
    print("  4. Exit")
    print("=" * 50)

def run_quiz_flow(score_manager):
    """Handles the user choices and execution for starting a quiz.""" # User choicex`any`

    clear_screen()
    print("\n" + "=" * 50)
    print("                   START A QUIZ")
    print("=" * 50)
    
    # Get user name

    while True:
        name = input("Enter your name: ").strip()
        if name:
            break
        print("Name cannot be empty.")

    # Select difficulty level

    print("\nSelect Difficulty Level:")
    print("  1. Easy")
    print("  2. Medium")
    print("  3. Hard")
    print("  4. Mixed (All levels)")
    diff_choice = get_valid_choice("Enter choice (1-4): ", ["1", "2", "3", "4"])
    
    difficulty_map = {
        "1": "Easy",
        "2": "Medium",
        "3": "Hard",
        "4": None
    }
    difficulty = difficulty_map[diff_choice]

    # Select timing option

    print("\nEnable 30-Second Question Timer?")
    print("  1. Yes (Recommended)")
    print("  2. No")
    timer_choice = get_valid_choice("Enter choice (1-2): ", ["1", "2"])
    use_timer = (timer_choice == "1")

    # Select randomization option

    print("\nRandomize Question Order?")
    print("  1. Yes (Recommended)")
    print("  2. No")
    rand_choice = get_valid_choice("Enter choice (1-2): ", ["1", "2"])
    randomize = (rand_choice == "1")

    # Create quiz

    quiz = Quiz(
        questions_file="questions.json",
        difficulty=difficulty,
        randomize=randomize,
        use_timer=use_timer
    )

    try:
        quiz.load_questions()
        
        # Check if we have enough questions
        # Minimum questions criteria is 10 for a full standard quiz,
        # but if we filter by difficulty, we might have fewer.
        # We'll allow taking the quiz anyway but notify the user.

        if len(quiz.questions) <= 10 and difficulty is not None:
            print(f"\nNote: Only {len(quiz.questions)} questions found for '{difficulty}' difficulty.")
            print("Quizzes usually require a minimum of 10 questions. You can add more in the Admin menu.")
            input("Press Enter to proceed with the available questions...")

        quiz.start(name)
        quiz.display_results()
        
        # Save score

        score_manager.save_result(quiz.results)
        print("Your score has been saved successfully!")
        
    except ValueError as ve:
        print(f"\nConfiguration Error: {ve}")
        print("Please check your questions.json or select a different difficulty.")
    except Exception as e:
        print(f"\nAn error occurred during the quiz: {e}")
        
    input("\nPress Enter to return to Main Menu...")

def add_new_question_flow():
    """Handles admin question adding flow with input validation.""" # For Adding New Questions

    clear_screen()
    print("\n" + "=" * 50)
    print("                 ADD NEW QUESTION")
    print("=" * 50)

    # Question text input

    while True:
        question_text = input("Enter the question text:\n> ").strip()
        if question_text:
            break
        print("Question text cannot be empty.")

    # Options A-D input

    options = {}
    for letter in ['A', 'B', 'C', 'D']:
        while True:
            opt = input(f"Enter Option {letter}:\n> ").strip()
            if opt:
                options[letter] = opt
                break
            print(f"Option {letter} cannot be empty.")

    # Correct Answer validation

    print("\nSelect the correct answer option:")
    correct_answer = get_valid_choice("Enter option letter (A/B/C/D): ", ['A', 'B', 'C', 'D'])

    # Difficulty validation

    print("\nSelect difficulty level:")
    diff_opt = get_valid_choice("Enter difficulty (Easy/Medium/Hard): ", ['Easy', 'Medium', 'Hard'])
    difficulty = diff_opt.capitalize()

    # Load existing questions to append

    questions_file = "questions.json"
    questions = []
    
    if os.path.exists(questions_file):
        try:
            with open(questions_file, 'r', encoding='utf-8') as f:
                questions = json.load(f)
        except json.JSONDecodeError:
            print("Warning: questions.json was corrupted. Creating a new list.")
        except Exception as e:
            print(f"Error reading questions.json: {e}")

    # Determine next ID

    next_id = 1
    if questions:

        # Filter out questions that don't have integer IDs or return max + 1

        ids = [q.get("id") for q in questions if isinstance(q.get("id"), int)]
        if ids:
            next_id = max(ids) + 1

    new_question = {
        "id": next_id,
        "question": question_text,
        "options": options,
        "correct_answer": correct_answer,
        "difficulty": difficulty
    }

    questions.append(new_question)

    # Save back to file

    try:
        with open(questions_file, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2)
        print("\nNew question added and saved successfully!")
    except Exception as e:
        print(f"\nError: Could not save the new question: {e}")

    input("\nPress Enter to return to Main Menu...")

def main():

    """Main execution entry point.""" # Main function
    score_manager = ScoreManager("scores.json")
    
    while True:
        try:
            show_main_menu()
            choice = get_valid_choice("Enter choice (1-4): ", ["1", "2", "3", "4"])
            
            if choice == "1":
                run_quiz_flow(score_manager)
            elif choice == "2":
                score_manager.display_previous_scores()
            elif choice == "3":
                add_new_question_flow()
            elif choice == "4":
                clear_screen()
                print("\nThank you for using the Console Quiz Application. Goodbye!\n")
                sys.exit(0)
        except KeyboardInterrupt:
            clear_screen()
            print("\nExiting program... Goodbye!\n")
            sys.exit(0)

if __name__ == "__main__":
    main()
