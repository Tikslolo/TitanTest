# TitanTest

## Last Light Gatekeeper (prototype)
A small game inspired by *Papers, Please* set in a post-apocalyptic survivor base.

You are the checkpoint guard. For each entrant, inspect clues and decide:
- **ALLOW** entry if they appear legitimate and safe.
- **DENY** if they seem bitten or are using a fake identity.

## Modes
### 1) Terminal mode
```bash
python3 guard_game.py
```

### 2) Interface mode (virtual people)
```bash
python3 guard_game_gui.py
```

The interface mode shows each entrant as a virtual character, with profile details and clues, then lets you click **ALLOW** or **DENY**.

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
