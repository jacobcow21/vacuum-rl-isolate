import ast
from pathlib import Path

import pytest

from src.agent import QLearningAgent
from src.train import greedy_rollout, train


def test_update_moves_q_toward_target():
    agent = QLearningAgent(alpha=0.5, gamma=0.9, epsilon=0.0, seed=0)
    agent.update((0, 0), "right", -0.04, (0, 1), done=False)
    # target = -0.04 + 0.9 * 0 = -0.04; new Q = 0 + 0.5 * (-0.04)
    assert agent.get_q((0, 0), "right") == pytest.approx(-0.02)


def test_terminal_update_ignores_future():
    agent = QLearningAgent(alpha=1.0, gamma=0.9, epsilon=0.0, seed=0)
    agent.q[((3, 3), "up")] = 100.0  # should not be used
    agent.update((2, 3), "down", 10.0, (3, 3), done=True)
    assert agent.get_q((2, 3), "down") == pytest.approx(10.0)


def test_epsilon_zero_is_greedy():
    agent = QLearningAgent(epsilon=0.0, seed=0)
    agent.q[((0, 0), "down")] = 1.0
    assert all(agent.choose_action((0, 0)) == "down" for _ in range(20))


def test_epsilon_one_explores_all_actions():
    agent = QLearningAgent(epsilon=1.0, seed=0)
    picks = {agent.choose_action((0, 0)) for _ in range(200)}
    assert picks == {"up", "down", "left", "right"}


def test_invalid_hyperparameters_rejected():
    with pytest.raises(ValueError):
        QLearningAgent(alpha=0)
    with pytest.raises(ValueError):
        QLearningAgent(gamma=1.5)


def test_trained_policy_reaches_goal_in_six_moves():
    agent, _, _ = train(seed=0)
    path, total, reached = greedy_rollout(agent)
    assert reached
    assert total == 10
    assert len(path) - 1 == 6
    assert (3, 1) not in path


@pytest.mark.parametrize("seed", [1, 2, 3, 4, 5])
def test_converges_across_seeds(seed):
    agent, _, _ = train(seed=seed)
    path, _, reached = greedy_rollout(agent)
    assert reached and len(path) - 1 == 6


def test_agent_does_not_import_hidden_model():
    """The agent must not see T or R (WALLS, TERMINAL_REWARDS)."""
    src = Path("src/agent.py").read_text()
    names = {
        alias.name
        for node in ast.walk(ast.parse(src))
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }
    assert not names & {"WALLS", "TERMINAL_REWARDS", "START", "*"}
