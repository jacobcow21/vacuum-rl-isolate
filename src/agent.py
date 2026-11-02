"""Q-learning agent for the vacuum robot.

Model-free: the agent never reads the grid layout or reward table. It only
learns from the (next_state, reward, done) tuples returned by env.step().

Update rule:

    Q(s, a) <- Q(s, a) + alpha * [ r + gamma * max_a' Q(s', a') - Q(s, a) ]

with the future term set to 0 when s' is terminal.
"""

from __future__ import annotations

import random

from src.environment import ACTIONS

State = tuple[int, int]


class QLearningAgent:
    def __init__(
        self,
        alpha: float = 0.5,
        gamma: float = 0.9,
        epsilon: float = 0.1,
        seed: int | None = None,
    ) -> None:
        if not 0 < alpha <= 1:
            raise ValueError("alpha must be in (0, 1]")
        if not 0 <= gamma <= 1:
            raise ValueError("gamma must be in [0, 1]")
        if not 0 <= epsilon <= 1:
            raise ValueError("epsilon must be in [0, 1]")
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.actions = ACTIONS
        self.rng = random.Random(seed)
        self.q: dict[tuple[State, str], float] = {}
        self.seen_states: set[State] = set()

    def get_q(self, state: State, action: str) -> float:
        return self.q.get((state, action), 0.0)

    def max_q(self, state: State) -> float:
        return max(self.get_q(state, a) for a in self.actions)

    def best_action(self, state: State) -> str:
        """Greedy action, ties broken randomly."""
        best = self.max_q(state)
        ties = [a for a in self.actions if self.get_q(state, a) == best]
        return self.rng.choice(ties)

    def choose_action(self, state: State) -> str:
        """Epsilon-greedy action selection."""
        self.seen_states.add(state)
        if self.rng.random() < self.epsilon:
            return self.rng.choice(self.actions)
        return self.best_action(state)

    def update(
        self,
        state: State,
        action: str,
        reward: float,
        next_state: State,
        done: bool,
    ) -> None:
        """Apply one Q-learning update."""
        future = 0.0 if done else self.max_q(next_state)
        target = reward + self.gamma * future
        old = self.get_q(state, action)
        self.q[(state, action)] = old + self.alpha * (target - old)
        self.seen_states.add(state)

    def greedy_policy(self) -> dict[State, str]:
        """Best action for every state the agent has visited.

        Ties are broken by ACTIONS order so the result is deterministic.
        """
        policy = {}
        for s in sorted(self.seen_states):
            policy[s] = max(self.actions, key=lambda a: self.get_q(s, a))
        return policy
