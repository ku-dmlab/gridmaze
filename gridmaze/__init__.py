import gym
from gridmaze.layouts import *

gym.register(
    id = "GridMaze-8x8-v0",
    entry_point = "gridmaze.gridmaze:GridMaze",
    kwargs={
        "layout": layout_8x8,
        "max_steps": 100,
    },
)

gym.register(
    id = "GridMaze-8x8-0-v0",
    entry_point = "gridmaze.gridmaze:GridMaze",
    kwargs={
        "layout": layout_8x8_0,
        "max_steps": 100,
    },
)

gym.register(
    id = "GridMaze-5x5-v0",
    entry_point = "gridmaze.gridmaze:GridMaze",
    kwargs={
        "layout": layout_5x5,
        "max_steps": 50,
    },
)