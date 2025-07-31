# shop.py

import json
import random
from typing import Callable, Dict

# ————————————————————————————————————————————————————————————————
# Data classes
# ————————————————————————————————————————————————————————————————

class ShopItem:
    """
    Represents a single boost in the shop.
    """
    def __init__(
        self,
        item_id: str,
        name: str,
        cost: int,
        description: str,
        effect: Callable[['Game'], None]
    ):
        self.id          = item_id
        self.name        = name
        self.cost        = cost
        self.description = description
        self.effect      = effect

# ————————————————————————————————————————————————————————————————
# Effect functions: call these to apply a boost to your Game
# ————————————————————————————————————————————————————————————————

def _effect_extra_guess(game):
    """
    Grant the player +1 allowed guess.
    Your Game class should handle this attribute (e.g. `self.max_guesses` or similar).
    """
    if hasattr(game, 'grant_extra_guess'):
        game.grant_extra_guess()
    else:
        # fallback: if you keep guesses in a list, you might increment a counter
        raise NotImplementedError("Game.grant_extra_guess() not implemented")

def _effect_reveal_random_letter(game):
    """
    Reveal a random *unrevealed* letter in the current puzzle grid.
    Your Game class needs to expose:
      - game.target (the solution word)
      - game.guesses / game.statuses so far
      - game.reveal_letter_at(index, status) or similar
    """
    if hasattr(game, 'reveal_random_letter'):
        game.reveal_random_letter()
    else:
        raise NotImplementedError("Game.reveal_random_letter() not implemented")

def _effect_reveal_one_letter(game):
    """
    Reveal one specific letter of your choice in its correct position.
    E.g. you may pop up a mini‐UI for the player to pick which letter to reveal.
    Your Game class should implement `reveal_one_letter()` accordingly.
    """
    if hasattr(game, 'reveal_one_letter'):
        game.reveal_one_letter()
    else:
        raise NotImplementedError("Game.reveal_one_letter() not implemented")

# ————————————————————————————————————————————————————————————————
# The shop catalog
# ————————————————————————————————————————————————————————————————

CATALOG: Dict[str, ShopItem] = {
    "extra_guess": ShopItem(
        item_id="extra_guess",
        name="Extra Guess",
        cost=100,
        description="Gives you one additional attempt on your next puzzle.",
        effect=_effect_extra_guess
    ),
    "reveal_random": ShopItem(
        item_id="reveal_random",
        name="Reveal Random Letter",
        cost=75,
        description="Automatically reveals one random letter in the current word.",
        effect=_effect_reveal_random_letter
    ),
    "reveal_one": ShopItem(
        item_id="reveal_one",
        name="Reveal One Letter",
        cost=50,
        description="Pick a position to reveal the correct letter.",
        effect=_effect_reveal_one_letter
    ),
}

# ————————————————————————————————————————————————————————————————
# Shop state, persistence, and logic
# ————————————————————————————————————————————————————————————————

_STATE_FILE = "shop_state.json"


class Shop:
    def __init__(self, state_file: str = _STATE_FILE):
        self.state_file = state_file

        # player currency
        self.coins: int = 0

        # how many of each item the player owns
        # e.g. { "extra_guess": 2, "reveal_one": 0, ... }
        self.inventory: Dict[str, int] = {item_id: 0 for item_id in CATALOG}

        self._load_state()

    def _load_state(self):
        """Attempt to load coins & inventory from disk."""
        try:
            data = json.load(open(self.state_file, "r"))
            self.coins     = data.get("coins", self.coins)
            inv            = data.get("inventory", {})
            for k, v in inv.items():
                if k in self.inventory:
                    self.inventory[k] = v
        except (FileNotFoundError, json.JSONDecodeError):
            # first run or corrupted file: ignore
            pass

    def save_state(self):
        """Persist coins & inventory back to disk."""
        data = {
            "coins":     self.coins,
            "inventory": self.inventory
        }
        with open(self.state_file, "w") as fp:
            json.dump(data, fp, indent=2)

    def earn_coins(self, amount: int):
        """Call when the player finishes a puzzle, etc."""
        self.coins += amount
        self.save_state()

    def can_afford(self, item_id: str) -> bool:
        item = CATALOG.get(item_id)
        return bool(item and self.coins >= item.cost)

    def purchase(self, item_id: str) -> bool:
        """
        Attempt to buy one unit of item_id.
        Returns True on success, False on insufficient funds or invalid ID.
        """
        item = CATALOG.get(item_id)
        if not item:
            return False

        if self.coins < item.cost:
            return False

        self.coins -= item.cost
        self.inventory[item_id] += 1
        self.save_state()
        return True

    def use(self, item_id: str, game) -> bool:
        """
        Redeem one unit of item_id and apply its effect to `game`.
        Returns True if used successfully, False otherwise.
        """
        if self.inventory.get(item_id, 0) < 1:
            return False

        shop_item = CATALOG[item_id]
        shop_item.effect(game)

        self.inventory[item_id] -= 1
        self.save_state()
        return True

    def get_catalog(self):
        """Return list of ShopItems for display in your UI."""
        return list(CATALOG.values())

    def get_balance(self) -> int:
        return self.coins

    def get_inventory(self) -> Dict[str, int]:
        return dict(self.inventory)
