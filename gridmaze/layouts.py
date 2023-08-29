# layout must be square
# there should be single agent and single goal
# - .: corridor
# - a: agent
# - g: goal
# - x: wall

layout_8x8 = """
    .a...x..
    xxx.xx.x
    .....x..
    .x.x...x
    ...x.xxx
    xx......
    .x.x.xx.
    .g......
    """ # 8x8 grid

layout_8x8_0 = """
    .a...x..
    xxx.xx.x
    .....x..
    .x.x...x
    .....xxx
    xx.x....
    .x.x.xx.
    .g......
    """ # 8x8 grid

layout_5x5 = """
    ...x.
    x.xa.
    ....x
    xx.x.
    ...g.
    """ # 5x5 grid