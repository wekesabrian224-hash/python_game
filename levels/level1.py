from utils import slow_print, menu, banner, pause


def play(state):
    banner("LEVEL 1 — THE AWAKENING")

    slow_print("You wake up on cold stone.")
    slow_print("There is blood on your sleeve.")
    slow_print("You don't remember whose it is.\n")
    slow_print('A voice whispers from the darkness:')
    slow_print('        "You came back."')

    choice = menu("What do you do?", [
        'Ask "Who are you?"',
        "Search the room",
        "Run toward the door",
    ])

    if choice == 0:
        slow_print('\nThe voice laughs, low and old.')
        slow_print('"You always ask that first."')
        state.nudge(curiosity=2, trust=-1)
    elif choice == 1:
        slow_print("\nYou search the cold floor and the walls.")
        state.nudge(curiosity=1, courage=1)
        _search_room(state)
    else:
        slow_print("\nYou bolt for the door. It's locked.")
        slow_print("Something about the panic feels... familiar.")
        state.nudge(courage=2, trust=-1)

    pause()

    # Ensure she finds the essentials regardless of path, but how she reacts differs
    if not state.flag("examined_symbol"):
        _find_symbol(state)

    if not state.flag("read_letter"):
        _find_letter(state)

    if "old key" not in state.inventory:
        state.add_item("old key")
        slow_print("\nYour fingers close around something metal in the dust: an old key.")
        pause()

    slow_print("\nA door groans open somewhere down the corridor.")
    slow_print("The dungeon is waiting.")
    pause()

    state.level = 2
    return state


def _search_room(state):
    slow_print("Beneath a loose stone, you find a folded letter and a carved symbol on the wall.")
    _find_letter(state)
    _find_symbol(state)


def _find_letter(state):
    if state.flag("read_letter"):
        return
    choice = menu("You find a mysterious letter, sealed in wax. Do you read it?", [
        "Read it",
        "Pocket it without reading",
    ])
    if choice == 0:
        slow_print('\nThe letter reads: "Forgive me. I did this to protect you."')
        slow_print("It isn't signed. The handwriting looks like yours.")
        state.set_flag("read_letter", True)
        state.nudge(curiosity=2)
    else:
        slow_print("\nYou fold it into your pocket, unread. It feels heavier than paper should.")
        state.add_item("sealed letter")
        state.nudge(trust=-1)


def _find_symbol(state):
    if state.flag("examined_symbol"):
        return
    choice = menu("A strange symbol is carved into the wall, still warm to the touch. Do you examine it closely?", [
        "Trace the symbol with your hand",
        "Ignore it and move on",
    ])
    if choice == 0:
        slow_print("\nThe moment you touch it, the torches flare violet, then dim.")
        slow_print('The whisper returns: "You remember more than you think."')
        state.set_flag("examined_symbol", True)
        state.nudge(curiosity=2, trust=1)
    else:
        slow_print("\nYou look away. Somehow, that feels like the wrong choice.")
        state.nudge(courage=-1)
