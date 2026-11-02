"""Train the Q-learning vacuum robot and print the result.

Usage (from the repo root):
    python -m src.train
    python -m src.train --living-reward -0.04 --gamma 0.9 --alpha 0.5 --epsilon 0.1
"""

from __future__ import annotations

import argparse

from src import config
from src.agent import QLearningAgent
from src.environment import ACTIONS, COLS, ROWS, VacuumGridEnv

ARROWS = {"up": "^", "down": "v", "left": "<", "right": ">"}


def train(
    living_reward: float = config.LIVING_REWARD,
    gamma: float = config.GAMMA,
    alpha: float = config.ALPHA,
    epsilon: float = config.EPSILON,
    episodes: int = config.EPISODES,
    max_steps: int = config.MAX_STEPS,
    seed: int = config.SEED,
    slip_prob: float = 0.0,
):
    """Run Q-learning. Returns (agent, env, per-episode returns)."""
    env = VacuumGridEnv(
        step_reward=living_reward,
        slip_prob=slip_prob,
        max_steps=max_steps,
        seed=seed,
    )
    agent = QLearningAgent(alpha=alpha, gamma=gamma, epsilon=epsilon, seed=seed)
    returns = []
    for _ in range(episodes):
        s = env.reset()
        done = False
        total = 0.0
        while not done:
            a = agent.choose_action(s)
            s2, r, done = env.step(a)
            agent.update(s, a, r, s2, done)
            total += r
            s = s2
        returns.append(total)
    return agent, env, returns


def greedy_rollout(agent: QLearningAgent, max_steps: int = 50):
    """Follow the greedy policy from the start with no exploration.

    Returns (path, total_reward, reached_goal).
    """
    env = VacuumGridEnv(step_reward=0.0, max_steps=max_steps)
    s = env.reset()
    path = [s]
    total = 0.0
    done = False
    policy = agent.greedy_policy()
    while not done:
        a = policy.get(s, ACTIONS[0])
        s, r, done = env.step(a)
        path.append(s)
        total += r
    return path, total, s == (3, 3)


def policy_grid(agent: QLearningAgent) -> str:
    policy = agent.greedy_policy()
    lines = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            s = (r, c)
            if s == (1, 1):
                row.append("X")
            elif s == (3, 1):
                row.append("-1")
            elif s == (3, 3):
                row.append("+10")
            else:
                row.append(ARROWS.get(policy.get(s, ""), "?"))
        lines.append(" ".join(f"{x:>3}" for x in row))
    return "\n".join(lines)


def value_grid(agent: QLearningAgent) -> str:
    lines = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            s = (r, c)
            if s == (1, 1):
                row.append("   X  ")
            elif s in ((3, 1), (3, 3)):
                row.append("  term")
            else:
                row.append(f"{agent.max_q(s):6.2f}")
        lines.append(" ".join(row))
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--living-reward", type=float, default=config.LIVING_REWARD)
    p.add_argument("--gamma", type=float, default=config.GAMMA)
    p.add_argument("--alpha", type=float, default=config.ALPHA)
    p.add_argument("--epsilon", type=float, default=config.EPSILON)
    p.add_argument("--episodes", type=int, default=config.EPISODES)
    p.add_argument("--seed", type=int, default=config.SEED)
    p.add_argument("--slip", type=float, default=0.0, help="slip probability")
    args = p.parse_args()

    agent, _, returns = train(
        living_reward=args.living_reward,
        gamma=args.gamma,
        alpha=args.alpha,
        epsilon=args.epsilon,
        episodes=args.episodes,
        seed=args.seed,
        slip_prob=args.slip,
    )
    path, _, reached = greedy_rollout(agent)
    last = returns[-50:]

    print(
        f"living_reward={args.living_reward}  gamma={args.gamma}  "
        f"alpha={args.alpha}  epsilon={args.epsilon}  episodes={args.episodes}"
    )
    print(f"\nAverage return, last 50 episodes: {sum(last) / len(last):.2f}")
    print("\nGreedy policy:")
    print(policy_grid(agent))
    print("\nState values  V(s) = max_a Q(s,a):")
    print(value_grid(agent))
    print(f"\nGreedy path from start ({len(path) - 1} moves): {path}")
    print("Reached +10:", reached)


if __name__ == "__main__":
    main()
