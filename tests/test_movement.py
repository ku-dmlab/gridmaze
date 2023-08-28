import os
import sys
import pytest
import gym
import numpy as np
from gym import spaces

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
sys.path.insert(0, PROJECT_DIR)

from gridmaze.gridmaze import GridMaze, Action

@pytest.fixture
def env_0():
    layout = """
    ...x.
    .xxa.
    ....x
    xx.x.
    ...g.
    """
    env = GridMaze(layout, 100)
    obs, info = env.reset()
    return env

def test_movement(env_0):
    env = env_0
    agent_loc = env._agent_location

    o, _, _, _ = env.step(Action(0)) # up
    assert agent_loc == o[0] # cannot move
    agent_loc = env._agent_location

    o, _, _, _ = env.step(Action(1)) # down
    assert agent_loc[0] + 1 == o[0][0]
    assert agent_loc[1] == o[0][1]
    agent_loc = env._agent_location

    o, _, _, _ = env.step(Action(2)) # left
    assert agent_loc[0] == o[0][0]
    assert agent_loc[1] - 1 == o[0][1]
    agent_loc = env._agent_location

    o, _, _, _ = env.step(Action(3)) # right
    assert agent_loc[0] == o[0][0]
    assert agent_loc[1] + 1 == o[0][1]

def test_reach_goal(env_0):
    env = env_0
    env.set_agent_location(4, 2)
    agent_loc = env._agent_location

    o, r, _, _ = env.step(Action(3)) # right
    assert agent_loc[0] == o[0][0]
    assert agent_loc[1] + 1 == o[0][1]
    assert r > 0