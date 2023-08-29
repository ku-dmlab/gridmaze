import os
import sys
import pytest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
sys.path.insert(0, PROJECT_DIR)

from gridmaze.gridmaze import GridMaze
from gridmaze.layouts import *

@pytest.fixture
def layout_0():
    layout = layout_8x8
    return layout

@pytest.fixture
def layout_1():
    layout = layout_5x5
    return layout

def test_layout(layout_0):
    layout = layout_0
    env = GridMaze(layout, 100)

    agent_loc = env._agent_location
    assert agent_loc == (0, 1)

    goal_loc = env._goal_location
    assert goal_loc == (7, 1)

@pytest.mark.skip(reason="Assertion")
def test_layout_1(layout_1):
    layout = layout_1
    env = GridMaze(layout, 100) # assertion here