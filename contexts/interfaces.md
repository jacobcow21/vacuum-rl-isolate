# Shared interfaces

This is the only file every role reads. Change it before changing any code
that crosses a boundary.

## Environment → everyone
```python
ACTIONS: tuple[str, ...] = ("up", "down", "left", "right")
State = tuple[int, int]  # (row, col)

class VacuumGridEnv:
    def reset(self) -> State
    def step(self, action: str) -> tuple[State, float, bool]  # (s', r, done)
    @staticmethod
    def states() -> list[State]
    @staticmethod
    def is_terminal(state: State) -> bool
    def render(self) -> str
```

## Agent → orchestrator / tester
```python
class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1, seed=None)
    def get_q(self, state, action) -> float
    def choose_action(self, state) -> str
    def update(self, state, action, reward, next_state, done) -> None
    def greedy_policy(self) -> dict[State, str]
```
