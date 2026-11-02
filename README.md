# Vacuum Robot RL — Lab 4: Q-learning (Isolate strategy)

A vacuum robot learns to reach the +10 cell in a 4x4 grid world. The
transition function T and reward function R are unknown, so the robot uses
model-free **Q-learning**: it learns only from the (next state, reward, done)
returned by each step.

```
start   0    0    0
  0     X    0    0
  0     0    0    0
  0    -1    0   10
```

## Result

```
$ python -m src.train
Greedy policy:                 State values V(s):
  >   >   v   v                 5.74   6.42   7.18   8.02
  ^   X   >   v                 5.12    X     8.02   8.96
  >   >   v   v                 0.82   6.29   8.96  10.00
  v  -1   > +10                -0.08   term  10.00   term

Greedy path (6 moves): (0,0) → (0,1) → (0,2) → (1,2) → (1,3) → (2,3) → (3,3)
Reached +10: True
```

The robot takes a shortest path (6 moves) and stays away from the -1 cell.
Cells in the bottom-left are visited rarely, so their values are less settled.

## Chosen values

| Parameter | Value | Why |
|---|---|---|
| Living reward | **-0.04** | A small cost per step pushes the robot toward short paths without changing the goal. With 0, rarely-visited states have no reason to hurry (79% optimal actions vs 93%). At -5, each step costs so much that the robot dives into the -1 cell to end the episode (0% reach +10). |
| Discount factor (γ) | **0.9** | +10 is 6 steps from the start; 0.9⁵ ≈ 0.59, so the goal still clearly matters there. Staying below 1 keeps values bounded and favors shorter paths; γ = 1.0 dropped to 87% optimal actions. |
| Learning rate (α) | **0.5** | Moves are deterministic, so there is no noise to average out. 0.5 found the optimal path by episode 11 vs 15 for α = 0.1, with the same final policy. (Use ~0.1 if slip is turned on.) |
| Epsilon (ε) | **0.1** | Balance between exploring and using what it has learned. ε = 0.01 explored too little (88% optimal actions); ε = 0.5 learned every state but averaged only 8.2 reward while training vs 9.6. |

Full numbers: [`results/sweep.md`](results/sweep.md) (10 seeds × 500 episodes per setting).

## Claude Code features used (3 of 4)

| Feature | Where | What it does |
|---|---|---|
| **Hooks** | `.claude/settings.json`, `.claude/hooks/` | *PreToolUse*: blocks any edit that makes `src/agent.py` use `WALLS`, `TERMINAL_REWARDS` or `START`, so the agent can't cheat by reading T and R. *PostToolUse*: runs `pytest` after every edit in `src/` or `tests/` and sends failures back to Claude. |
| **Skills** | `.claude/skills/` | `train-vacuum-agent`: how to train, what a good result looks like, and how to report it. `tune-hyperparameters`: how to run the sweep, read it, and pick values. |
| **Sub-agents** | `.claude/agents/` | `env-builder`, `rl-agent-builder`, `tester`, `hyperparameter-tuner`, each with its own limited context. The agent builder never sees the grid layout, just like the robot. |

MCP was not used.

## Project structure

```
.
├── CLAUDE.md                     # Orchestrator: delegates to sub-agents
├── README.md
├── requirements.txt              # pytest
├── pytest.ini
├── .claude/
│   ├── settings.json             # Hook configuration
│   ├── hooks/
│   │   ├── guard_agent_model.py  # PreToolUse: keep T and R out of the agent
│   │   └── run_tests.py          # PostToolUse: run tests after edits
│   ├── skills/
│   │   ├── train-vacuum-agent/SKILL.md
│   │   └── tune-hyperparameters/SKILL.md
│   └── agents/
│       ├── env-builder.md
│       ├── rl-agent-builder.md
│       ├── tester.md
│       └── hyperparameter-tuner.md
├── contexts/                     # Per-role context (Isolate strategy)
│   ├── interfaces.md             # Shared contract, read by all roles
│   ├── env.md
│   ├── agent.md
│   └── testing.md
├── src/
│   ├── environment.py            # Grid world: reset(), step(), render()
│   ├── agent.py                  # Q-learning agent
│   ├── config.py                 # Chosen hyperparameters
│   └── train.py                  # Training loop and printed results
├── scripts/
│   └── sweep.py                  # Hyperparameter sweep
├── results/
│   └── sweep.md                  # Sweep output
└── tests/
    ├── test_environment.py       # 8 tests
    └── test_agent.py             # 12 tests
```

## Run

```bash
pip install -r requirements.txt
python -m src.train                    # train with the chosen values
python -m src.train --living-reward -5 # see the robot dive into -1
python -m scripts.sweep                # rerun the sweep (~5 s)
pytest                                 # 20 tests
```

## Q-learning update

```
Q(s,a) ← Q(s,a) + α [ r + γ · max_a' Q(s',a') − Q(s,a) ]
```

The future term is 0 when s' is terminal. Actions are chosen epsilon-greedy.
