import pytest

from src.environment import START, VacuumGridEnv


def test_reset_returns_start():
    env = VacuumGridEnv()
    assert env.reset() == START


def test_edge_bump_stays_in_place():
    env = VacuumGridEnv()
    env.reset()
    state, reward, done = env.step("up")
    assert state == START and reward == 0 and not done


def test_wall_blocks_movement():
    env = VacuumGridEnv()
    env.reset()
    env.step("right")  # (0, 1)
    state, _, _ = env.step("down")  # (1, 1) is the wall
    assert state == (0, 1)


def test_goal_gives_plus_ten_and_ends():
    env = VacuumGridEnv()
    env.reset()
    for a in ["right", "right", "right", "down", "down"]:
        env.step(a)
    state, reward, done = env.step("down")
    assert state == (3, 3) and reward == 10 and done


def test_penalty_gives_minus_one_and_ends():
    env = VacuumGridEnv()
    env.reset()
    for a in ["down", "down", "down"]:
        env.step(a)
    state, reward, done = env.step("right")
    assert state == (3, 1) and reward == -1 and done


def test_step_after_done_raises():
    env = VacuumGridEnv()
    env.reset()
    for a in ["down", "down", "down", "right"]:
        env.step(a)
    with pytest.raises(RuntimeError):
        env.step("up")


def test_max_steps_cutoff():
    env = VacuumGridEnv(max_steps=3)
    env.reset()
    env.step("up")
    env.step("up")
    _, _, done = env.step("up")
    assert done


def test_states_excludes_wall():
    states = VacuumGridEnv.states()
    assert (1, 1) not in states and len(states) == 15
