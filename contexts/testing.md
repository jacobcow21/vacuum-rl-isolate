# Testing context (tester only)

- pytest, run from repo root (`pytest.ini` sets the path).
- Test only through public APIs in `contexts/interfaces.md`.
- Existing: `tests/test_environment.py` (8 tests: reset, bumps, wall, both
  terminals, step after done, cutoff, state list).
- To add next lab: a single-update test for `QLearningAgent.update`, and a
  seeded convergence test that the greedy path from (0,0) reaches (3,3) in
  6 moves.
- Report back: pass/fail counts and any failing test names. No full logs.
