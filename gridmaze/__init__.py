import gym

layout_8x8 = """
    a....x..
    xxx.xx.x
    .....x..
    .x.x...x
    ...x.xxx
    xx.x....
    .x.xxxx.
    .g......
    """ # 8x8 grid

layout_5x5 = """
    ...x.
    .xxa.
    ....x
    xx.x.
    ...g.
    """ # 5x5 grid

gym.register(
    id = "GridMaze-8x8-v0",
    entry_point = "gridmaze.gridmaze:GridMaze",
    kwargs={
        "layout": layout_8x8,
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