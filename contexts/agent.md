# Agent context (rl-agent-builder only)

You don't know the grid layout, where the rewards are, or how actions move
the robot. You only have the interface in `contexts/interfaces.md`. That's
the point: the robot learns T and R implicitly through experience.

## Q-learning
```
Q(s,a) <- Q(s,a) + alpha * [ r + gamma * max_a' Q(s',a') - Q(s,a) ]
```
- Use 0 for the future term when `done` is True.
- Epsilon-greedy action choice; break ties randomly with the seeded RNG.
- Q-table: dict keyed by `(state, action)`, default 0.0.

## Training loop
```python
s = env.reset(); done = False
while not done:
    a = agent.choose_action(s)
    s2, r, done = env.step(a)
    agent.update(s, a, r, s2, done)
    s = s2
```
