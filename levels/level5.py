from utils import slow_print, menu, banner, pause


def play(state):
    banner("LEVEL 5 — THE HEART OF THE DUNGEON")

    slow_print("The passage ends in a vast chamber, lit by nothing you can name.")
    slow_print("At its center: a throne of black stone, and a chain, and a door shaped like an eye.")

    slow_print("\nThe voice no longer whispers. It speaks plainly, in a voice uncomfortably like your own:")
    slow_print('"You didn\'t escape into this place. You were never taken. You built the lock, Elara."')

    if state.flag("accepted_truth"):
        slow_print('\n"...I know," you hear yourself say, before you decide to say it.')
        slow_print("Somewhere, a memory surfaces: you, older, exhausted, sealing something vast beneath the stone.")
    else:
        slow_print("\nYou want to deny it. The words won't come. Some part of you already knew.")

    slow_print("\nThe throne waits. The chain waits. The eye-shaped door waits.")
    pause()

    ending = _determine_ending(state)
    _narrate_ending(ending, state)
    state.level = 6  # signal completion to the main loop
    return ending


def _determine_ending(state):
    t = state.traits
    trust, courage, curiosity = t["trust"], t["courage"], t["curiosity"]
    f = state.flags

    # The New Keeper: she accepts the truth of who she is and chooses to stay in control of it
    if f.get("accepted_truth") and (f.get("completed_ritual") or f.get("listened")) and trust >= 2:
        return "keeper"

    # The Sacrifice: high courage, willing to destroy it even at cost to herself,
    # especially if she broke the ritual or has low trust in the dungeon's offer
    if f.get("broke_ritual") and courage >= 3:
        return "sacrifice"
    if courage >= 5 and trust <= 0:
        return "sacrifice"

    # The Dungeon Wins: she refused to face the truth, or trust collapsed entirely
    if not f.get("accepted_truth") and curiosity <= 1:
        return "loop"
    if trust <= -3:
        return "loop"

    # Escape: the default — she gets out, changed but intact
    return "escape"


def _narrate_ending(ending, state):
    if ending == "escape":
        banner("🩸 ENDING — THE ESCAPE")
        slow_print("You turn from the throne and run for the eye-shaped door.")
        slow_print("Stone grinds behind you, but you don't look back.")
        slow_print("\nDaylight — real, blinding daylight — hits your face.")
        slow_print("You made it out. Whatever you were to this place, you leave it behind.")
        if state.flags.get("ally") == "girl":
            slow_print("\nThe girl's charm is still warm in your pocket. You never learn her name.")
        slow_print("\nBut some nights, you still dream of cold stone.")

    elif ending == "sacrifice":
        banner("🔥 ENDING — THE SACRIFICE")
        slow_print("You understand, finally, what escaping would cost everyone else.")
        slow_print("You take the chain in your hands and pull the chamber down around you both.")
        slow_print("\nThe dungeon screams — a sound like a thousand years exhaling at once.")
        slow_print("It ends here. It ends with you.")
        slow_print("\nSomewhere above, sunlight touches a doorway that will never open again.")
        slow_print("No one will know what you did. That was always the price.")

    elif ending == "keeper":
        banner("👑 ENDING — THE NEW KEEPER")
        slow_print("You sit on the throne of black stone — not as a prisoner, but as a choice.")
        slow_print('"I remember now," you say. "I remember why I stayed the first time, too."')
        slow_print("\nThe dungeon quiets around you, familiar now instead of hostile.")
        slow_print("You are not trapped here. You are the one holding the door shut.")
        slow_print("Somewhere far above, the world continues, safe, because you chose to remain.")

    else:  # loop
        banner("🔄 ENDING — THE DUNGEON WINS")
        slow_print("You run. You find the door. You burst through it into blinding light.")
        slow_print("Relief floods through you — until the light fades, and the cold stone returns.")
        slow_print("\nYou wake up on cold stone.")
        slow_print("There is blood on your sleeve.")
        slow_print("You don't remember whose it is.")
        slow_print('\nA voice whispers from the darkness:')
        slow_print('        "You came back."')
        state.flags["loops"] = state.flags.get("loops", 0) + 1

    pause("\n(press Enter to finish)")
