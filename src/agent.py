"""Q-learning agent for the vacuum robot (to be implemented in a later lab).

Only the interface is defined here. The update rule to implement is:

    Q(s, a) <- Q(s, a) + alpha * [ r + gamma * max_a' Q(s', a') - Q(s, a) ]

with Q(s', .) treated as 0 when s' is terminal.
"""

from __future__ import annotations

from src.environment import ACTIONS


class QLearningAgent:
    def __init__(
        self,
        alpha: float = 0.1,
        gamma: float = 0.9,
        epsilon: float = 0.1,
        seed: int | None = None,
    ) -> None:
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.seed = seed
        self.actions = ACTIONS
        self.q: dict[tuple[tuple[int, int], str], float] = {}

    def get_q(self, state, action) -> float:
        return self.q.get((state, action), 0.0)

    def choose_action(self, state) -> str:
        """Epsilon-greedy action selection."""
        raise NotImplementedError("Implement in the Q-learning lab.")

    def update(self, state, action, reward, next_state, done) -> None:
        """Apply one Q-learning update."""
        raise NotImplementedError("Implement in the Q-learning lab.")

    def greedy_policy(self) -> dict:
        """Return the best action for each state."""
        raise NotImplementedError("Implement in the Q-learning lab.")
