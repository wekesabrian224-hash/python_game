from utils import slow_print, menu, banner, pause


def play(state):
    banner("LEVEL 4 — THE RITUAL CHAMBER")

    slow_print("The walls here are not stone. They pulse, faintly, like something breathing.")
    slow_print("This is not a building. It never was.")

    ally_present = state.flags.get("ally") == "girl"
    if ally_present:
        slow_print('\nThe girl stops at the threshold. "I can\'t go further," she says. "It won\'t let me."')
        slow_print("She presses something into your hand before stepping back into the dark.")
        state.add_item("girl's charm")

    # Which doors are available depends on earlier choices
    doors = ["The door that hums with the binding symbol"]
    if state.flag("questioned_girl"):
        doors.append("The door marked with a name you almost recognize")
    if state.flag("pulled_lever"):
        doors.append("The door the lever unlocked, cold air seeping from beneath it")
    doors.append("The plain door nobody would think to choose")

    choice = menu("Three — or more — doors stand before you. Which do you take?", doors)
    chosen = doors[choice]
    state.flags["ritual_door"] = chosen
    slow_print(f"\nYou step through: {chosen}")

    if "binding symbol" in chosen:
        slow_print("Runes flare up your arms, matching the mark from Level 1.")
        slow_print("Whatever this place is sealing, it recognizes you as part of the lock.")
        state.nudge(trust=1, curiosity=1)
    elif "almost recognize" in chosen:
        slow_print("The name on the door is a version of your own, worn smooth by time.")
        slow_print("You realize with a cold certainty: this isn't the first door like this you've opened.")
        state.set_flag("saw_old_name", True)
        state.nudge(curiosity=2)
    elif "lever unlocked" in chosen:
        slow_print("The passage is freezing. Something down here has been waiting a long time.")
        state.nudge(courage=1)
    else:
        slow_print("The plain door was never plain. Behind it, the truth was just... waiting to be noticed.")
        state.nudge(curiosity=1, trust=-1)

    pause()

    slow_print("\nAt the center of the chamber, a ritual circle waits, half-finished.")
    slow_print("Completing it would take something from you. Refusing it might too.")

    final_choice = menu("The circle pulses, waiting for a decision.", [
        "Complete the ritual",
        "Break the circle instead",
        "Wait — do nothing, and listen to what the dungeon wants",
    ])

    if final_choice == 0:
        slow_print("\nYou kneel and finish the pattern. The room exhales.")
        state.set_flag("completed_ritual", True)
        state.nudge(trust=2, courage=1)
    elif final_choice == 1:
        slow_print("\nYou scatter the circle with your foot. The pulse in the walls stutters, angry.")
        state.set_flag("broke_ritual", True)
        state.nudge(courage=2, trust=-2)
    else:
        slow_print('\nThe voice returns, closer now: "...Finally. You\'re listening."')
        state.set_flag("listened", True)
        state.nudge(curiosity=2)

    pause()
    state.level = 5
    return state
