import json
import os

class ScoreManager:
    def __init__(self, scores_file="scores.json"):
        self.scores_file = scores_file

    def _load_scores(self):
        """Loads scores from file, handling errors gracefully."""

        if not os.path.exists(self.scores_file):
            return []
        try:
            with open(self.scores_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Warning: Score file is corrupted. Resetting data.")
            return []
        except Exception as e:
            print(f"Error reading scores file: {e}")
            return []

    def _save_scores(self, scores):
        """Saves scores to file."""

        try:
            with open(self.scores_file, 'w', encoding='utf-8') as f:
                json.dump(scores, f, indent=2)
        except Exception as e:
            print(f"Error saving scores file: {e}")

    def save_result(self, quiz_results):
        """Saves a quiz result to the database."""

        scores = self._load_scores()
        scores.append(quiz_results)
        self._save_scores(scores)

    def display_previous_scores(self):
        """Displays all previous quiz attempts and summary statistics."""

        scores = self._load_scores()
        
        if not scores:
            print("\nNo quiz history found yet. Take a quiz to record scores!")
            input("\nPress Enter to return to Main Menu...")
            return

        print("\n" + "=" * 65)
        print("                        PREVIOUS QUIZ ATTEMPTS")
        print("=" * 65)
        print(f"{'Date/Time':<20} | {'Name':<15} | {'Score':<6} | {'Percentage':<10} | {'Status':<6}")
        print("-" * 65)
        
        percentages = []
        for attempt in scores:
            dt = attempt.get("datetime", "N/A")
            name = attempt.get("name", "Unknown")
            score_str = f"{attempt.get('correct_answers', 0)}/{attempt.get('total_questions', 0)}"
            pct = attempt.get("percentage", 0.0)
            status = attempt.get("status", "FAIL")
            percentages.append(pct)
            
            print(f"{dt:<20} | {name:<15} | {score_str:<6} | {pct:>9}% | {status:<6}")
            
        print("=" * 65)
        
        # Calculate and show overall metrics

        total_attempts = len(scores)
        highest_pct = max(percentages) if percentages else 0.0
        average_pct = sum(percentages) / total_attempts if total_attempts > 0 else 0.0
        
        print(f"Total Attempts: {total_attempts}")
        print(f"Highest Score:  {highest_pct}%")
        print(f"Average Score:  {round(average_pct, 2)}%")
        print("=" * 65)
        
        # Show Top 10 Leaderboard

        self.display_leaderboard(scores)
        
        input("\nPress Enter to return to Main Menu...")

    def display_leaderboard(self, scores=None):
        """Displays the Top 10 Leaderboard based on score percentages."""
        if scores is None:
            scores = self._load_scores()

        if not scores:
            return

        print("\n" + "=" * 50)
        print("                 TOP 10 LEADERBOARD")
        print("=" * 50)
        print(f"{'Rank':<5} | {'Name':<20} | {'Score':<8} | {'Percentage':<10}")
        print("-" * 50)

        # Sort scores: primary key = percentage desc, secondary key = datetime desc
        sorted_scores = sorted(
            scores,
            key=lambda x: (x.get("percentage", 0.0), x.get("datetime", "")),
            reverse=True
        )

        for rank, attempt in enumerate(sorted_scores[:10], 1): # FOR ranking users (top 10)
            name = attempt.get("name", "Unknown")
            score_str = f"{attempt.get('correct_answers', 0)}/{attempt.get('total_questions', 0)}"
            pct = attempt.get("percentage", 0.0)
            print(f"{rank:<5} | {name:<20} | {score_str:<8} | {pct:>9}%")
            
        print("=" * 50)
