# Environment context (env-builder only)

Grid, (row, col), row 0 on top:

```
S  .  .  .
.  X  .  .
.  .  .  .
. -1  . +10
```

- Start (0,0). Wall (1,1).
- (3,1): -1, terminal. (3,3): +10, terminal. Others: `step_reward` (default 0).
- Edge or wall bump: stay in place.
- `slip_prob` (default 0): perpendicular slip chance.
- `max_steps` (default 100): episode cutoff.

These internals (`WALLS`, `TERMINAL_REWARDS`) are the hidden T and R. They
must not appear in `contexts/agent.md` or be imported by `src/agent.py`.
