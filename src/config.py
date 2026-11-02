"""Chosen hyperparameters for Lab 4.

See README.md ("Chosen values") and results/sweep.md for why.
"""

LIVING_REWARD = -0.04   # reward for every non-terminal step
GAMMA = 0.9             # discount factor
ALPHA = 0.5             # learning rate
EPSILON = 0.1           # exploration rate (epsilon-greedy)

EPISODES = 500
MAX_STEPS = 100
SEED = 0
