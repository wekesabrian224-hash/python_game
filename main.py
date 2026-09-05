#!/usr/bin/env python3
"""
THE DUNGEON REMEMBERS
A choice-driven CLI adventure in 5 levels.

Run with: python main.py
"""

from game_state import GameState
from utils import clear, slow_print, banner, menu, pause
from levels import level1, level2, level3, level4, level5

LEVELS = [level1, level2, level3, level4, level5]


def title_screen():
    clear()
    print(r"""
    ╔══════════════════════════════════╗
    ║          THE DUNGEON             ║
    ║          REMEMBERS               ║
    ╚══════════════════════════════════╝

            👧 ELARA
    """)
    saved = GameState.load()
    options = ["New Game"]
    if saved:
        options.append("Continue")
    options.append("Quit")

    choice = menu("What do you do?", options)
    label = options[choice]

    if label == "Quit":
        slow_print("\nThe dungeon settles back into silence.")
        raise SystemExit
    if label == "Continue":
        return saved
    GameState.clear_save()
    return GameState()


def run():
    state = title_screen()

    while state.level <= 5:
        module = LEVELS[state.level - 1]
        clear()
        result = module.play(state)
        state.save()

        if state.level > 5:
            # level5.play returns the ending string instead of state
            _handle_post_ending(result, state)
            return

    # Should not normally reach here, but handle defensively
    print("\nThe dungeon falls quiet.")


def _handle_post_ending(ending, state):
    if ending == "loop":
        replay = menu("\nPlay through the loop again?", ["Yes — go again", "No — stop here"])
        if replay == 0:
            state.level = 1
            # Keep traits/flags — the dungeon remembers, even across loops
            run_loop(state)
        else:
            GameState.clear_save()
    else:
        slow_print("\nTHE END")
        GameState.clear_save()


def run_loop(state):
    while state.level <= 5:
        module = LEVELS[state.level - 1]
        clear()
        result = module.play(state)
        state.save()
        if state.level > 5:
            _handle_post_ending(result, state)
            return


if __name__ == "__main__":
    try:
        run()
    except (KeyboardInterrupt, EOFError):
        print("\n\nThe dungeon lets you go... for now.")
