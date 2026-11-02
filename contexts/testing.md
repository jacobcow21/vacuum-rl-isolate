# Testing context (tester only)

- pytest, run from repo root (`pytest.ini` sets the path).
- Test only through public APIs in `contexts/interfaces.md`.
- `tests/test_environment.py` (8 tests): reset, bumps, wall, both terminals,
  step after done, cutoff, state list.
- `tests/test_agent.py` (12 tests): single Q update, terminal update,
  epsilon 0 and 1, invalid hyperparameters, greedy path reaches +10 in 6
  moves (seeds 0–5), agent does not import the hidden model.
- The PostToolUse hook runs the suite after every edit.
- Report back: pass/fail counts and any failing test names. No full logs.
