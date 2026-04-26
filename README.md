# TitanTest

## Last Light Gatekeeper (prototype)
A small game inspired by *Papers, Please* set in a post-apocalyptic survivor base.

You are the checkpoint guard. For each entrant, inspect clues and decide:
- **ALLOW** entry if they appear legitimate and safe.
- **DENY** if they seem bitten or are using a fake identity.

## Run
### Recommended (opens interface mode)
```bash
python3 guard_game.py
```

### Explicit modes
```bash
python3 guard_game.py --mode gui
python3 guard_game.py --mode cli
```

## If the game window/terminal closes immediately
- Use `python3 guard_game.py` to start in GUI mode by default.
- If GUI cannot start, the program falls back to CLI and prints the reason.
- If you launch from a file explorer, use a terminal so you can see error messages.

### Current mechanics
- Randomized entrants with hidden states:
  - legitimate survivor
  - bitten survivor
  - fake identity/impostor
- Virtual entrant profiles (avatar emoji, age, occupation)
- Clue-based inspection each round
- Score + strike tracking
- Multi-day shift and final outcome report

### Tests
```bash
python3 -m unittest -v
```
