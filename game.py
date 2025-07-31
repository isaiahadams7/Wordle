# game.py
import random
from config import GRID_SIZE, WORD_LENGTH

def load_word_list(path="words.txt"):
    """Load valid guess/answer words from a file."""
    with open(path, "r") as f:
        return [w.strip().lower() for w in f if len(w.strip()) == WORD_LENGTH]

class Game:
    def __init__(self, word_list):
        self.word_list = word_list
        self.reset()

    def reset(self):
        self.target = random.choice(self.word_list)
        self.guesses = []
        self.results = []
        self.current_guess = ""
        self.won = False
        self.over = False

    def add_letter(self, letter):
        if len(self.current_guess) < WORD_LENGTH:
            self.current_guess += letter

    def remove_letter(self):
        self.current_guess = self.current_guess[:-1]

    def submit_guess(self):
        if len(self.current_guess) != WORD_LENGTH:
            return False

        guess = self.current_guess.lower()
        if guess not in self.word_list:
            return False

        status = []
        for i, ch in enumerate(guess):
            if ch == self.target[i]:
                status.append("correct")
            elif ch in self.target:
                status.append("present")
            else:
                status.append("absent")

        self.guesses.append(guess)
        self.results.append(status)

        if guess == self.target:
            self.won = True
            self.over = True
        elif len(self.guesses) >= GRID_SIZE:
            self.over = True

        self.current_guess = ""
        return True

    def is_over(self):
        return self.over

    def is_won(self):
        return self.won
