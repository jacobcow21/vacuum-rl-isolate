---
name: train-vacuum-agent
description: Train the Q-learning vacuum robot and report its learned policy, state values, and greedy path. Use when asked to train, run, or check the agent.
---

# Train the vacuum robot

1. From the repo root, run:
   ```bash
   python -m src.train
   ```
   This uses the chosen values in `src/config.py`
   (living reward -0.04, gamma 0.9, alpha 0.5, epsilon 0.1, 500 episodes).

2. To try other values, pass flags:
   ```bash
   python -m src.train --living-reward -0.5 --gamma 0.99 --alpha 0.1 --epsilon 0.3 --episodes 1000 --seed 1
   ```
   Add `--slip 0.2` to test a noisy (stochastic) robot.

3. Check the output:
   - **Greedy path** should be 6 moves from (0,0) to (3,3) and never touch (3,1).
   - **Reached +10** should be `True`.
   - **Average return** over the last 50 episodes should be close to 10 minus
     the living-reward cost (about 9.6 with the defaults; lower is expected
     because epsilon keeps exploring).

4. Report back in this format:
   ```
   Values: living=…, gamma=…, alpha=…, epsilon=…
   Path: N moves, reached +10: yes/no
   Avg return (last 50): …
   Policy grid: (paste the 4 lines)
   ```

Do not change `src/config.py` here. Changing the chosen values is the job of
the `tune-hyperparameters` skill.
