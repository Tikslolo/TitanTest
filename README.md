# TitanTest

## Last Light Gatekeeper (prototype)
A small terminal game inspired by *Papers, Please* set in a post-apocalyptic survivor base.

You are the checkpoint guard. For each entrant, inspect clues and decide:
- **ALLOW** entry if they appear legitimate and safe.
- **DENY** if they seem bitten or are using a fake identity.

### Run
```bash
python3 guard_game.py
```

### Current mechanics
- Randomized entrants with hidden states:
  - legitimate survivor
  - bitten survivor
  - fake identity/impostor
- Clue-based inspection text each round
- Score + strike tracking
- Multiple day loop and final outcome report
