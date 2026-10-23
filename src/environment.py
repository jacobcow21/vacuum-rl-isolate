"""Vacuum robot grid world.

Layout (row 0 is the top row, column 0 is the left column):

    start   0    0    0
      0     X    0    0
      0     0    0    0
      0    -1    0   10

- "start" is (0, 0).
- X at (1, 1) is an obstacle the robot cannot enter.
- (3, 1) gives -1 and ends the episode.
- (3, 3) gives +10 and ends the episode.
- Every other cell gives 0.

The agent is NOT given the transition function T or the reward function R.
It only sees (state, reward, done) after each step, which is why the plan
is to use model-free Q-learning.
"""

from __future__ import annotations

import random
from typing import Optional

ROWS = 4
COLS = 4
START = (0, 0)
WALLS = {(1, 1)}
TERMINAL_REWARDS = {(3, 1): -1.0, (3, 3): 10.0}

ACTIONS = ("up", "down", "left", "right")
_MOVES = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}


class VacuumGridEnv:
    """Small episodic grid world with an unknown (to the agent) model.

    Args:
        step_reward: reward for entering a non-terminal cell (default 0,
            matching the grid in the assignment).
        slip_prob: chance the robot moves in a random perpendicular
            direction instead of the chosen one. 0 means deterministic.
        max_steps: episode cutoff so a bad policy cannot loop forever.
        seed: optional seed for reproducible slips.
    """

    def __init__(
        self,
        step_reward: float = 0.0,
        slip_prob: float = 0.0,
        max_steps: int = 100,
        seed: Optional[int] = None,
    ) -> None:
        if not 0.0 <= slip_prob <= 1.0:
            raise ValueError("slip_prob must be between 0 and 1")
        self.step_reward = step_reward
        self.slip_prob = slip_prob
        self.max_steps = max_steps
        self.rng = random.Random(seed)
        self.state = START
        self.steps = 0
        self.done = False

    # ------------------------------------------------------------------ API
    def reset(self) -> tuple[int, int]:
        self.state = START
        self.steps = 0
        self.done = False
        return self.state

    def step(self, action: str) -> tuple[tuple[int, int], float, bool]:
        """Apply an action and return (next_state, reward, done)."""
        if self.done:
            raise RuntimeError("Episode finished; call reset() first.")
        if action not in _MOVES:
            raise ValueError(f"Unknown action {action!r}; use one of {ACTIONS}")

        actual = self._maybe_slip(action)
        dr, dc = _MOVES[actual]
        r, c = self.state
        nxt = (r + dr, c + dc)

        # Bumping into the edge or the wall leaves the robot in place.
        if not self._in_bounds(nxt) or nxt in WALLS:
            nxt = self.state

        self.state = nxt
        self.steps += 1

        if nxt in TERMINAL_REWARDS:
            reward = TERMINAL_REWARDS[nxt]
            self.done = True
        else:
            reward = self.step_reward
            self.done = self.steps >= self.max_steps

        return nxt, reward, self.done

    # -------------------------------------------------------------- helpers
    @staticmethod
    def states() -> list[tuple[int, int]]:
        """All cells the robot can occupy (excludes walls)."""
        return [
            (r, c)
            for r in range(ROWS)
            for c in range(COLS)
            if (r, c) not in WALLS
        ]

    @staticmethod
    def is_terminal(state: tuple[int, int]) -> bool:
        return state in TERMINAL_REWARDS

    def render(self) -> str:
        rows = []
        for r in range(ROWS):
            cells = []
            for c in range(COLS):
                pos = (r, c)
                if pos == self.state:
                    cells.append("R")
                elif pos in WALLS:
                    cells.append("X")
                elif pos in TERMINAL_REWARDS:
                    cells.append(f"{TERMINAL_REWARDS[pos]:+g}")
                elif pos == START:
                    cells.append("S")
                else:
                    cells.append(".")
            rows.append(" ".join(f"{x:>3}" for x in cells))
        return "\n".join(rows)

    def _maybe_slip(self, action: str) -> str:
        if self.slip_prob == 0.0 or self.rng.random() >= self.slip_prob:
            return action
        if action in ("up", "down"):
            return self.rng.choice(("left", "right"))
        return self.rng.choice(("up", "down"))

    @staticmethod
    def _in_bounds(pos: tuple[int, int]) -> bool:
        r, c = pos
        return 0 <= r < ROWS and 0 <= c < COLS


if __name__ == "__main__":
    env = VacuumGridEnv()
    env.reset()
    print(env.render())
