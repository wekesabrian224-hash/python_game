# The Dungeon Remembers

A 5-level, choice-driven CLI adventure. Elara's decisions in early levels
alter dialogue, available paths, and which of 4 endings she reaches.

## Run it

```bash
python main.py
```

Requires Python 3.7+. No external dependencies.

## Structure

```
dungeon_remembers/
├── main.py            # title screen, game loop, save/continue handling
├── game_state.py       # GameState: inventory, flags, traits, JSON save/load
├── utils.py            # slow_print, menu(), banner(), clear()
└── levels/
    ├── level1.py       # The Awakening
    ├── level2.py       # The Prison
    ├── level3.py       # The Forgotten Library
    ├── level4.py       # The Ritual Chamber
    └── level5.py       # The Heart of the Dungeon + ending logic
```

## How memory works

Two mechanisms drive "the dungeon remembers":

- **`flags`** (dict of booleans/strings) — discrete story beats: did she
  rescue the girl in Level 2? Did she accept the truth in Level 3?
  Which ritual door did she pick in Level 4?
- **`traits`** (numeric: `trust`, `courage`, `curiosity`) — nudged up or
  down by nearly every choice, and used alongside flags to weight the
  final ending in `level5._determine_ending()`.

Progress autosaves to `elara_save.json` after every level, so `Continue`
on the title screen resumes mid-run.

## The 4 endings

Ending selection (`levels/level5.py::_determine_ending`) is a simple
priority chain over flags + trait thresholds:

1. **👑 The New Keeper** — accepted the truth, completed/embraced the
   ritual, and trust is high.
2. **🔥 The Sacrifice** — broke the ritual with high courage, or high
   courage paired with low trust.
3. **🔄 The Dungeon Wins** — never accepted the truth and stayed
   incurious, or trust collapsed. Loops back to Level 1, carrying flags
   and traits forward (the dungeon remembers the loop too).
4. **🩸 The Escape** — the default outcome for anyone who doesn't hit
   the above thresholds.

## Extending it

- Add new flags/traits in `GameState`, then read/write them in any level.
- Add a new door or ending branch by extending the lists/if-chains in
  `level4.py` / `level5.py` — nothing elsewhere needs to change.
- Want harder branching? Replace the flat trait ints with a weighted
  scoring function, or add a `personality()` method to `GameState` that
  classifies the player into an archetype other levels can query.
