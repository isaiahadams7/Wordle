# game.py
import random
from config import WORD_LENGTH, GRID_SIZE
import os

class Game:
    def __init__(self):
        # Load your 5-letter words from words.txt
        base = os.path.dirname(__file__)
        path = os.path.join(base, 'words.txt')
        with open(path, 'r') as f:
            words = [w.strip().lower() for w in f if len(w.strip()) == WORD_LENGTH]

        # Use set for fast lookup, list for random choice
        self.dictionary    = set(words)
        self.solution_list = list(self.dictionary)

        # Pick a random target for this practice run
        self.target        = random.choice(self.solution_list)
        self.guesses       = []     # all submitted guesses
        self.results       = []     # parallel list of status-lists
        self.current_guess = ""     # letters the player is typing
        self.key_states    = {}     # letter -> best status seen

    def add_letter(self, ch: str):
        """Append a letter to the current guess (capped at WORD_LENGTH)."""
        if len(self.current_guess) < WORD_LENGTH:
            self.current_guess += ch.lower()

    def remove_letter(self):
        """Remove the last letter from the current guess."""
        self.current_guess = self.current_guess[:-1]

    def submit_guess(self) -> bool:
        """
        Validate and score the current guess.
        Returns True if the guess was valid and scored, False otherwise.
        """
        guess = self.current_guess.lower()

        # 1) Check length
        if len(guess) != WORD_LENGTH:
            return False

        # 2) Check dictionary
        if guess not in self.dictionary:
            return False

        # 3) Score it: build a list of 'correct', 'present', 'absent'
        status = ['absent'] * WORD_LENGTH
        target_chars = list(self.target)

        # First pass: mark greens
        for i, ch in enumerate(guess):
            if ch == target_chars[i]:
                status[i] = 'correct'
                target_chars[i] = None  # consume this letter

        # Build counts of remaining letters in target
        counts = {}
        for ch in target_chars:
            if ch:
                counts[ch] = counts.get(ch, 0) + 1

        # Second pass: mark yellows
        for i, ch in enumerate(guess):
            if status[i] == 'absent' and counts.get(ch, 0) > 0:
                status[i] = 'present'
                counts[ch] -= 1

        # 4) Record the guess & result
        self.guesses.append(guess)
        self.results.append(status)
        self.current_guess = ""

        # 5) Update on-screen keyboard states (never downgrade)
        priority = {'absent': 0, 'present': 1, 'correct': 2}
        for ch, st in zip(guess, status):
            prev = self.key_states.get(ch)
            if not prev or priority[st] > priority[prev]:
                self.key_states[ch] = st

        return True

    def is_over(self) -> bool:
        """Returns True if player has won or used up all attempts."""
        return self.is_won() or len(self.guesses) >= GRID_SIZE

    def is_won(self) -> bool:
        """Returns True if the last guess exactly matched the target."""
        return bool(self.guesses and self.guesses[-1] == self.target)
