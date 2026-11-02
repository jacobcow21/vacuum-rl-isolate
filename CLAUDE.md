# Orchestrator instructions

You coordinate work on a Q-learning vacuum robot. Do not do implementation
work yourself. Delegate to the subagent whose scope fits, and keep only their
short reports in your context.

## Subagents (`.claude/agents/`)
- `env-builder`: anything in `src/environment.py`
- `rl-agent-builder`: `src/agent.py`, `src/train.py`
- `tester`: writing and running tests
- `hyperparameter-tuner`: living reward, gamma, alpha, epsilon (`src/config.py`)

## Skills (`.claude/skills/`)
- `train-vacuum-agent`: train and report the learned policy
- `tune-hyperparameters`: run the sweep and justify values

## Hooks (`.claude/settings.json`)
- PreToolUse: blocks edits that make `src/agent.py` use the hidden model
  (`WALLS`, `TERMINAL_REWARDS`, `START`).
- PostToolUse: runs `pytest` after any edit in `src/` or `tests/`; failures
  come back to you.

## How to delegate
1. Give the subagent one task and point it to `contexts/interfaces.md`.
2. Ask for a report of at most 5 lines: what changed, test result, open issues.
3. If a change crosses roles (e.g. a new env method the agent needs), update
   `contexts/interfaces.md` first, then delegate each side separately.

## Task list
- [x] Environment built and tested (env-builder, tester)
- [x] Epsilon-greedy and Q-learning update (rl-agent-builder)
- [x] Training script and convergence tests (rl-agent-builder, tester)
- [x] Hyperparameters chosen from sweep (hyperparameter-tuner)
- [ ] Optional: test with `--slip 0.2` and retune alpha
