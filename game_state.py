"""
game_state.py
Central memory of the game: everything Elara has done, found, and become.
This is the "the dungeon remembers" mechanism — every level reads and writes here.
"""

from dataclasses import dataclass, field, asdict
import json
import os

SAVE_FILE = "elara_save.json"


@dataclass
class GameState:
    # Inventory
    inventory: list = field(default_factory=list)

    # Discrete story flags (set once, never scored)
    flags: dict = field(default_factory=lambda: {
        "read_letter": False,
        "examined_symbol": False,
        "rescued_girl": False,
        "left_girl": False,
        "questioned_girl": False,
        "found_own_book": False,
        "accepted_truth": False,
        "ritual_door": None,      # which door she opened in Level 4
        "ally": None,             # who is with her by Level 5 ("girl" / None)
        "loops": 0,               # how many times she's looped (Ending 4 tracking)
    })

    # Continuous traits, nudged by choices, drive tone + ending weight
    traits: dict = field(default_factory=lambda: {
        "trust": 0,      # trust in others / the dungeon's voice
        "courage": 0,    # boldness vs caution
        "curiosity": 0,  # digs for truth vs avoids it
    })

    level: int = 1

    # --- helpers -----------------------------------------------------

    def add_item(self, item: str):
        if item not in self.inventory:
            self.inventory.append(item)

    def has_item(self, item: str) -> bool:
        return item in self.inventory

    def nudge(self, trust=0, courage=0, curiosity=0):
        self.traits["trust"] += trust
        self.traits["courage"] += courage
        self.traits["curiosity"] += curiosity

    def set_flag(self, key, value=True):
        self.flags[key] = value

    def flag(self, key):
        return self.flags.get(key)

    # --- persistence ---------------------------------------------------

    def save(self, path=SAVE_FILE):
        with open(path, "w") as f:
            json.dump(asdict(self), f, indent=2)

    @classmethod
    def load(cls, path=SAVE_FILE):
        if not os.path.exists(path):
            return None
        with open(path) as f:
            data = json.load(f)
        state = cls()
        state.inventory = data.get("inventory", [])
        state.flags.update(data.get("flags", {}))
        state.traits.update(data.get("traits", {}))
        state.level = data.get("level", 1)
        return state

    @staticmethod
    def clear_save(path=SAVE_FILE):
        if os.path.exists(path):
            os.remove(path)
