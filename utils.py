"""
utils.py
Small presentation helpers: typewriter text, menus, screen clearing.
"""

import time
import sys
import os


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def slow_print(text: str, delay: float = 0.018, end="\n"):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)


def pause(prompt="\n(press Enter to continue)"):
    input(prompt)


def banner(title: str):
    width = max(36, len(title) + 8)
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width + "\n")


def menu(prompt: str, options: list) -> int:
    """
    Prints a numbered menu and returns the 0-indexed choice.
    options: list of strings.
    """
    slow_print(prompt)
    print()
    for i, opt in enumerate(options, start=1):
        print(f"  {i}. {opt}")
    print()
    while True:
        raw = input("> ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return int(raw) - 1
        print(f"Choose a number between 1 and {len(options)}.")
