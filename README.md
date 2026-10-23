# Vacuum Robot RL — Context Strategy: **Isolate**

A vacuum robot learns to reach the +10 cell in a 4x4 grid world. The transition
function T and reward function R are unknown, so the robot will use model-free
Q-learning (implemented in a later lab).

```
start   0    0    0
  0     X    0    0
  0     0    0    0
  0    -1    0   10
```

## The strategy

**Isolate** means splitting context across separate agents (or separate
sessions) so each one sees only what its job needs. A main orchestrator hands
out tasks to subagents, each with its own narrow context window, and gets
back short results instead of everything they read.

| File | Role | Sees |
|------|------|------|
| `CLAUDE.md` | Orchestrator | Task list, interfaces, subagent results |
| `.claude/agents/env-builder.md` | Environment subagent | `src/environment.py`, `contexts/env.md` |
| `.claude/agents/rl-agent-builder.md` | Agent subagent | `src/agent.py`, `contexts/agent.md`, env **interface only** |
| `.claude/agents/tester.md` | Testing subagent | `tests/`, `contexts/testing.md`, public APIs |
| `contexts/interfaces.md` | Shared contract | The only thing all roles share |

This mirrors the RL problem itself: the agent subagent is isolated from the
environment's internals in the same way the Q-learning robot can't see T and R.

## Project layout

```
src/environment.py        Grid world (reset, step, render)
src/agent.py              Q-learning agent interface (stub)
tests/                    pytest tests for the environment
contexts/                 Per-role context files
.claude/agents/           Subagent definitions (the strategy)
CLAUDE.md                 Orchestrator instructions
```

## Run

```bash
pip install -r requirements.txt
python -m src.environment   # print the grid
pytest                      # run tests
```
