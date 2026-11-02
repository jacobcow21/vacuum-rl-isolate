---
name: tune-hyperparameters
description: Sweep living reward, discount factor, learning rate, and epsilon for the vacuum robot and justify the chosen values. Use when asked to tune, compare, or explain hyperparameters.
---

# Tune hyperparameters

## 1. Run the sweep
```bash
python -m scripts.sweep > results/sweep.md
```
It changes one value at a time around `src/config.py`, runs 10 seeds of 500
episodes each, and writes a markdown table per parameter.

## 2. Read the columns
| Column | Meaning | Want |
|---|---|---|
| goal% | runs whose greedy path reaches +10 in 6 moves | 100 |
| policy% | states whose learned action is optimal (checked against value iteration, evaluation only) | high |
| first optimal episode | how fast the start-state path became optimal | low |
| avg return (last 50) | reward collected while still exploring | high |

## 3. Pick values with these rules
- **Living reward**: small negative. 0 gives no push toward short paths in
  rarely-visited states; very negative (around -5) makes the robot dive into
  the -1 cell to end the episode early.
- **Gamma**: high enough that +10 still matters 6 steps away
  (0.9^5 ≈ 0.59), below 1 so values stay bounded and shorter paths win.
- **Alpha**: the environment is deterministic, so a larger rate learns
  faster without noisy averaging. Lower it (e.g. 0.1) if `--slip` > 0.
- **Epsilon**: trade-off. Higher explores more states (better policy%) but
  costs return during training.

## 4. Apply
- Update `src/config.py`.
- Run `pytest` (the PostToolUse hook also does this after edits).
- Update the "Chosen values" table in `README.md` with the new numbers.
