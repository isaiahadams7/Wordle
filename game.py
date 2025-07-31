# game.py

import random
import json
import os
from config import WORD_LENGTH, GRID_SIZE

# Where stats are persisted
STATS_FILE = 'stats.json'

class Game:
    def __init__(self):
        # load valid words
        with open('words.txt') as f:
            self.words = [
                w.strip().upper()
                for w in f
                if len(w.strip()) == WORD_LENGTH
            ]

        # pick a target
        self.target = random.choice(self.words)

        # game state
        self.guesses        = []     # list of submitted guesses
        self.results        = []     # parallel list of per‐letter statuses
        self.current_guess  = ""     # what the player is typing now
        self.key_states     = {}     # for coloring the on-screen keyboard

        # boost‐related state
        self.max_guesses    = GRID_SIZE   # can be bumped by Extra Try


    def add_letter(self, ch):
        if len(self.current_guess) < WORD_LENGTH and ch.isalpha():
            self.current_guess += ch.upper()

    def remove_letter(self):
        self.current_guess = self.current_guess[:-1]

    def is_won(self):
        return any(
            guess == self.target
            for guess in self.guesses
        )

    def is_over(self):
        # either guessed correctly or used up all allowed rows
        return self.is_won() or len(self.guesses) >= self.max_guesses

    def submit_guess(self):
        # must be full length and in word list
        if len(self.current_guess) != WORD_LENGTH:
            return False
        if self.current_guess not in self.words:
            return False

        # commit the guess
        guess = self.current_guess
        self.guesses.append(guess)

        # evaluate result
        status = []
        target_chars = list(self.target)
        # first pass: correct spots
        for i, ch in enumerate(guess):
            if ch == target_chars[i]:
                status.append('correct')
                target_chars[i] = None
            else:
                status.append(None)

        # second pass: present vs absent
        for i, ch in enumerate(guess):
            if status[i] is None:
                if ch in target_chars:
                    status[i] = 'present'
                    target_chars[target_chars.index(ch)] = None
                else:
                    status[i] = 'absent'
        self.results.append(status)

        # update keyboard colors
        for i, ch in enumerate(guess):
            prev = self.key_states.get(ch.lower())
            # don't override a correct with a lesser state
            if prev == 'correct':
                continue
            self.key_states[ch.lower()] = status[i]

        # reset current guess
        self.current_guess = ""

        # if the game just ended, bump stats
        if self.is_over():
            self._update_stats(self.is_won())

        return True

    def _update_stats(self, won):
        """
        Load stats.json (or create defaults), increment wins/losses,
        and rewrite the file. Awards coins on win if a Shop has been injected.
        """
        data = {'wins': 0, 'losses': 0}
        try:
            if os.path.exists(STATS_FILE):
                with open(STATS_FILE, 'r') as fp:
                    data = json.load(fp)
        except (json.JSONDecodeError, IOError):
            data = {'wins': 0, 'losses': 0}

        if won:
            data['wins'] = data.get('wins', 0) + 1
            # award coins if shop is attached
            if hasattr(self, 'shop'):
                self.shop.earn_coins(25)
        else:
            data['losses'] = data.get('losses', 0) + 1

        try:
            with open(STATS_FILE, 'w') as fp:
                json.dump(data, fp, indent=2)
        except IOError:
            pass


    # ─── Boost Hooks ─────────────────────────────────────────────────

    def reveal_letter(self):
        """
        Reveal a random letter from the target by marking it 'correct' on the keyboard.
        Returns the letter, or None if everything is already revealed.
        """
        candidates = [
            ch for ch in set(self.target)
            if self.key_states.get(ch.lower()) != 'correct'
        ]
        if not candidates:
            return None

        letter = random.choice(candidates)
        self.key_states[letter.lower()] = 'correct'
        return letter


    def grant_extra_guess(self):
        """
        Increase the number of allowed guesses by one.
        """
        self.max_guesses += 1


    def freeze_timer(self):
        """
        Placeholder for a “freeze” effect. If you have a timer in GameUI,
        call its pause/unpause methods from your GameUI.freeze_timer().
        """
        pass
