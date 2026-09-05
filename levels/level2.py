from utils import slow_print, menu, banner, pause


def play(state):
    banner("LEVEL 2 — THE PRISON")

    slow_print("The corridor opens into a row of cells, doors hanging off rusted hinges.")
    slow_print("In the last cell, something moves.")
    slow_print('A girl, thin and pale, presses against the bars.')
    slow_print('"Don\'t trust the dungeon," she hisses.')

    if state.flag("examined_symbol"):
        slow_print("\nShe flinches when she sees the mark still glowing faintly on your palm.")
        slow_print('"You... you\'re one of them, aren\'t you."')

    choice = menu("What do you do?", [
        "Rescue her — pick the lock with the old key",
        "Leave her — something feels wrong here",
        "Question her before deciding",
    ])

    if choice == 0:
        slow_print("\nThe key fits. The lock groans open.")
        slow_print('"Thank you," she whispers. "I\'ll help you however I can."')
        state.set_flag("rescued_girl", True)
        state.flags["ally"] = "girl"
        state.nudge(trust=2, courage=1)
    elif choice == 1:
        slow_print("\nYou step back. Her eyes widen, but she doesn't beg.")
        slow_print('"...Smart," she mutters, almost to herself.')
        state.set_flag("left_girl", True)
        state.nudge(trust=-2, courage=-1)
    else:
        slow_print("\nYou keep your distance and ask her what she knows.")
        _question_her(state)

    pause()

    slow_print("\nDeeper in the prison block, you find a rusted lever and a second locked door.")
    lever_choice = menu("A lever juts from the wall, half-broken. Do you pull it?", [
        "Pull the lever",
        "Leave it alone",
    ])
    if lever_choice == 0:
        slow_print("\nGears grind somewhere below. A distant door unlocks — or does something else unlock too?")
        state.set_flag("pulled_lever", True)
        state.nudge(courage=1, curiosity=1)
    else:
        slow_print("\nYou leave the mechanism untouched. Some things should stay buried.")
        state.nudge(trust=1)

    pause()
    state.level = 3
    return state


def _question_her(state):
    slow_print('\n"What is this place?" you ask.')
    slow_print('She studies you for a long moment.')
    slow_print('"It remembers everyone who\'s ever tried to leave. It remembers YOU."')

    follow_up = menu('"What do you mean, remembers me?"', [
        "Press her for more",
        "Back away — you're not ready to hear this",
    ])
    if follow_up == 0:
        slow_print('\n"You\'ve been here before," she says. "More than once. It always resets."')
        state.set_flag("questioned_girl", True)
        state.nudge(curiosity=2, trust=1)
    else:
        slow_print("\nYou turn away before she can say more. The words follow you anyway.")
        state.set_flag("questioned_girl", True)
        state.nudge(curiosity=1, courage=-1)
