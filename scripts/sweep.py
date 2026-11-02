"""Hyperparameter sweep for the Q-learning vacuum robot.

Varies one value at a time around the chosen config and reports, over
several seeds:

- goal%      : runs whose greedy path from start reaches +10 in 6 moves
- policy%    : states where the learned action is optimal (checked against
               value iteration on the true model; the AGENT never sees this
               model, only this evaluation script does)
- first_opt  : average episode at which the greedy path first became optimal
- avg_return : average return over the last 50 training episodes

Usage (from repo root):
    python -m scripts.sweep            # prints a markdown report
    python -m scripts.sweep > results/sweep.md
"""

from __future__ import annotations

from statistics import mean

from src import config
from src.agent import QLearningAgent
from src.environment import (
    ACTIONS,
    COLS,
    ROWS,
    START,
    TERMINAL_REWARDS,
    WALLS,
    VacuumGridEnv,
)

SEEDS = range(10)
EPISODES = config.EPISODES
MOVES = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
GOAL = (3, 3)


# ----------------------------------------------------- ground truth (eval only)
def _next(s, a):
    r, c = s
    dr, dc = MOVES[a]
    n = (r + dr, c + dc)
    if not (0 <= n[0] < ROWS and 0 <= n[1] < COLS) or n in WALLS:
        return s
    return n


def _reward(n, living):
    return TERMINAL_REWARDS.get(n, living)


def optimal_actions(living, gamma, iters=500):
    states = VacuumGridEnv.states()
    v = {s: 0.0 for s in states}

    def q(s, a):
        n = _next(s, a)
        future = 0.0 if n in TERMINAL_REWARDS else v[n]
        return _reward(n, living) + gamma * future

    for _ in range(iters):
        v = {
            s: 0.0 if s in TERMINAL_REWARDS else max(q(s, a) for a in ACTIONS)
            for s in states
        }
    best = {}
    for s in states:
        if s in TERMINAL_REWARDS:
            continue
        qs = {a: q(s, a) for a in ACTIONS}
        top = max(qs.values())
        best[s] = {a for a, val in qs.items() if abs(val - top) < 1e-9}
    return best


# ------------------------------------------------------------------ one run
def greedy_path_ok(agent):
    s, seen = START, set()
    for _ in range(20):
        if s in TERMINAL_REWARDS:
            break
        seen.add(s)
        a = max(ACTIONS, key=lambda x: agent.get_q(s, x))
        s = _next(s, a)
    return s == GOAL and len(seen) == 6


def run(living, gamma, alpha, epsilon, seed):
    env = VacuumGridEnv(step_reward=living, max_steps=config.MAX_STEPS, seed=seed)
    agent = QLearningAgent(alpha=alpha, gamma=gamma, epsilon=epsilon, seed=seed)
    returns, first_opt = [], None
    for ep in range(EPISODES):
        s, done, total = env.reset(), False, 0.0
        while not done:
            a = agent.choose_action(s)
            s2, r, done = env.step(a)
            agent.update(s, a, r, s2, done)
            total += r
            s = s2
        returns.append(total)
        if first_opt is None and greedy_path_ok(agent):
            first_opt = ep + 1
    best = optimal_actions(living, gamma)
    match = mean(
        1.0 if max(ACTIONS, key=lambda a: agent.get_q(s, a)) in acts else 0.0
        for s, acts in best.items()
    )
    return {
        "goal": greedy_path_ok(agent),
        "policy": match,
        "first_opt": first_opt if first_opt is not None else EPISODES,
        "ret": mean(returns[-50:]),
    }


def summarize(living, gamma, alpha, epsilon):
    rs = [run(living, gamma, alpha, epsilon, s) for s in SEEDS]
    return (
        100 * mean(r["goal"] for r in rs),
        100 * mean(r["policy"] for r in rs),
        mean(r["first_opt"] for r in rs),
        mean(r["ret"] for r in rs),
    )


SWEEPS = {
    "living_reward": [0.0, -0.04, -0.5, -2.0, -5.0],
    "gamma": [0.5, 0.9, 0.99, 1.0],
    "alpha": [0.1, 0.5, 0.9],
    "epsilon": [0.01, 0.1, 0.3, 0.5],
}


def main():
    base = {
        "living_reward": config.LIVING_REWARD,
        "gamma": config.GAMMA,
        "alpha": config.ALPHA,
        "epsilon": config.EPSILON,
    }
    print("# Hyperparameter sweep\n")
    print(
        f"Baseline: living_reward={base['living_reward']}, gamma={base['gamma']}, "
        f"alpha={base['alpha']}, epsilon={base['epsilon']}. "
        f"{EPISODES} episodes, {len(SEEDS)} seeds per setting. "
        "One value changes at a time.\n"
    )
    for name, values in SWEEPS.items():
        print(f"## {name}\n")
        print("| value | goal% | policy% | first optimal episode | avg return (last 50) |")
        print("|---|---|---|---|---|")
        for v in values:
            params = dict(base, **{name: v})
            g, p, f, r = summarize(
                params["living_reward"], params["gamma"],
                params["alpha"], params["epsilon"],
            )
            mark = " **(chosen)**" if v == base[name] else ""
            print(f"| {v}{mark} | {g:.0f} | {p:.0f} | {f:.0f} | {r:.2f} |")
        print()


if __name__ == "__main__":
    main()
