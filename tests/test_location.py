import os
import sys
import pytest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
sys.path.insert(0, PROJECT_DIR)

from gridmaze.gridmaze import GridMaze
from gridmaze.layouts import *

@pytest.fixture
def env_0():
    layout = layout_8x8 # 8x8 grid
    env = GridMaze(layout, 100)
    obs, info = env.reset()
    return env

@pytest.fixture
def env_1():
    layout = layout_5x5
    env = GridMaze(layout, 100)
    obs, info = env.reset()
    return env

@pytest.mark.skip(reason="Assertion")
def test_set_gloal_location(env_0):
    env = env_0
    env.set_goal_location(3, 5) # row, col
    env.set_goal_location(6, 1) # assertion here

@pytest.mark.skip(reason="Assertion")
def test_set_agent_location(env_0):
    env = env_0
    env.set_agent_location(2, 0)
    env.set_agent_location(4, 3) # assertion here

def test_set_location(env_1):
    env = env_1
    indices = [(0,0), (0,1), (0,2), (0,4),
                (1,1), (1,3), (1,4),
                (2,0), (2,1), (2,2), (2,3),
                (3,2), (3, 4),
                (4,0), (4,1), (4,2), (4,3), (4,4)]

    for (x, y) in indices:
        env.set_goal_location(x, y)
    
    for (x, y) in indices:
        env.set_agent_location(x, y)
