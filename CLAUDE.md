# Orchestrator instructions

You coordinate work on a Q-learning vacuum robot. Do not do implementation
work yourself. Delegate to the subagent whose scope fits, and keep only their
short reports in your context.

## Subagents
- `env-builder`: anything in `src/environment.py`
- `rl-agent-builder`: anything in `src/agent.py` or the training loop
- `tester`: writing and running tests

## How to delegate
1. Give the subagent one task and point it to `contexts/interfaces.md`.
2. Ask for a report of at most 5 lines: what changed, test result, open issues.
3. If a change crosses roles (e.g. a new env method the agent needs), update
   `contexts/interfaces.md` first, then delegate each side separately.

## Current task list
- [x] Environment built and tested (env-builder, tester)
- [x] Agent interface stub (rl-agent-builder)
- [ ] Implement epsilon-greedy and Q update (rl-agent-builder) — next lab
- [ ] Training script and convergence test (rl-agent-builder, tester) — next lab
