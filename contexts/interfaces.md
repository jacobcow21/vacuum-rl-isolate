# Shared interfaces

This is the only file every role reads. Change it before changing any code
that crosses a boundary.

## Environment → everyone
```python
ACTIONS: tuple[str, ...] = ("up", "down", "left", "right")
State = tuple[int, int]  # (row, col)

class VacuumGridEnv:
    def __init__(self, step_reward=0.0, slip_prob=0.0, max_steps=100, seed=None)
    def reset(self) -> State
    def step(self, action: str) -> tuple[State, float, bool]  # (s', r, done)
    @staticmethod
    def states() -> list[State]
    @staticmethod
    def is_terminal(state: State) -> bool
    def render(self) -> str
```
`step_reward` is the **living reward**.

## Agent → orchestrator / tester
```python
class QLearningAgent:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.1, seed=None)
    def get_q(self, state, action) -> float
    def max_q(self, state) -> float
    def choose_action(self, state) -> str          # epsilon-greedy
    def update(self, state, action, reward, next_state, done) -> None
    def greedy_policy(self) -> dict[State, str]
```

## Training (src/train.py)
```python
def train(living_reward, gamma, alpha, epsilon, episodes, max_steps, seed, slip_prob)
    -> (agent, env, returns)
def greedy_rollout(agent, max_steps=50) -> (path, total_reward, reached_goal)
```

## Config (src/config.py)
`LIVING_REWARD`, `GAMMA`, `ALPHA`, `EPSILON`, `EPISODES`, `MAX_STEPS`, `SEED`
