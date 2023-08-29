import gym
from gym import spaces
import pygame
import numpy as np
from enum import Enum
from typing import List, Tuple, Optional, Dict

_WHITE = (255, 255, 255)
_RED = (255, 0, 0)
_GREEN = (0, 255, 0)
_BLACK = (0, 0, 0)

COLOR_BACKGROUND = _WHITE
COLOR_GOAL = _RED
COLOR_AGENT = _GREEN
COLOR_WALL = _BLACK

class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Agent:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.req_action: Optional[Action] = None

    def req_location(self, grid_size) -> Tuple[int, int]:
        """
        (0,0) ... (0,H)
          :         :
        (W,0) ... (W,H)
        """
        if self.req_action == Action.UP:
            return max(0, self.x - 1), self.y
        elif self.req_action == Action.DOWN:
            return min(grid_size[1] - 1, self.x + 1), self.y
        elif self.req_action == Action.LEFT:
            return self.x, max(0, self.y - 1)
        elif self.req_action == Action.RIGHT:
            return self.x, min(grid_size[0] - 1, self.y + 1)
        
        raise ValueError(
            f"Action is {self.req_action}. Should be one of {[v for v in Action]}"
        )

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def get_location(self):
        return (self.x, self.y)

class GridMaze(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, layout: str, max_steps: Optional[int], render_mode: Optional[str]=None):
        self._goal_location: Tuple[int, int] = ()
        self._agent_location: Tuple[int, int] = ()

        self.layout = layout
        self._make_layout_from_str(self.layout)

        self.action_space = spaces.Discrete(len(Action))
        self.observation_space = spaces.Dict({"agent": spaces.MultiDiscrete([self.grid_size[0], self.grid_size[1]])})

        self._cur_steps = 0
        self.max_steps = max_steps

        # render settings
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.clock = None
        self.window = None
        self.window_size = 512
    
    def _make_layout_from_str(self, layout):
        layout = layout.strip()
        layout = layout.replace(" ", "")
        grid_height = layout.count("\n") + 1
        lines = layout.split("\n")
        grid_width = len(lines[0])
        for line in lines:
            assert grid_height == grid_width, "Layout must be square"

        self.grid_size = (grid_width, grid_height)
        self.corridors = np.zeros(self.grid_size, dtype=np.int32)

        cnt = 0
        for x, line in enumerate(lines):
            for y, char in enumerate(line):
                assert char.lower() in "agx."
                if char.lower() == "g": # goal
                    self._goal_location = (x, y)
                    self.corridors[x, y] = 1
                elif char.lower() == ".": # corridor
                    self.corridors[x, y] = 1
                elif char.lower() == "x": # wall
                    cnt += 1
                elif char.lower() == "a": # agent
                    self._agent_location = (x, y)
                    self.corridors[x, y] = 1

        self.n_walls = cnt

        assert self._goal_location != (), "Goal is required"
        assert self._agent_location != (), "Agent is required"

    def _is_corridor(self, x: int, y: int) -> bool:
        return self.corridors[x, y]
    
    def _get_obs(self):
        return [self._agent_location]
    
    def _get_info(self):
        return {"distance": np.linalg.norm(np.array(self._agent_location) - np.array(self._goal_location), ord=1)}
    
    def set_goal_location(self, x, y):
        assert self._is_corridor(x, y), f"({x}, {y}) is on walls"
        self._goal_location = (x, y)

    def set_agent_location(self, x, y):
        assert self._is_corridor(x, y), f"({x}, {y}) is on walls"
        self.agent.set_location(x, y)
        self._agent_location = self.agent.get_location()
    
    def reset(self) -> Tuple[List, Dict]:
        self._cur_steps = 0

        self._make_layout_from_str(self.layout)

        self.agent = Agent(*self._agent_location)

        obs = self._get_obs()
        info = self._get_info()

        return obs, info

    def step(self, action: Action) -> Tuple[List, float, bool, Dict]:
        self._cur_steps += 1
        reward = 0.
        done = False

        self.agent.req_action = Action(action)
        # act
        x, y = self.agent.req_location(self.grid_size)
        if self._is_corridor(x, y): # possible to move
            self.set_agent_location(x, y)

        # calculate goal reward
        if self._agent_location == self._goal_location:
            reward += 1.
            done = True

        # terminate
        if self.max_steps and self._cur_steps >= self.max_steps:
            done = True
            
        obs = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return obs, reward, done, info
    
    def render(self, render_mode="rgb_array"):
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        if self.render_mode == "rgb_array":
            return self._render_frame()
        else: # human
            self._render_frame()

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))

        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()
        
        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill(COLOR_BACKGROUND)
        # the size of a single grid square in pixels
        pix_square_size = (self.window_size / self.grid_size[0])

        # draw gridlines
        for x in range(self.grid_size[0] + 1):
            pygame.draw.line(
                canvas,
                0,
                (0, pix_square_size * x),
                (self.window_size, pix_square_size * x),
                width=2,
            )
            pygame.draw.line(
                canvas,
                0,
                (pix_square_size * x, 0),
                (pix_square_size * x, self.window_size),
                width=2,
            )

        # draw the goal
        pygame.draw.circle(
            canvas,
            COLOR_GOAL,
            (np.array(self._goal_location) + 0.5) * pix_square_size,
            pix_square_size / 3,
        )

        # draw the agent
        pygame.draw.circle(
            canvas,
            COLOR_AGENT,
            (np.array(self._agent_location) + 0.5) * pix_square_size,
            pix_square_size / 3,
        )

        # draw the walls
        for y, x in zip(
            np.indices(self.grid_size)[0].reshape(-1),
            np.indices(self.grid_size)[1].reshape(-1)
        ):
            if not self._is_corridor(x, y):
                pygame.draw.rect(
                    canvas,
                    COLOR_WALL,
                    pygame.Rect(
                        pix_square_size * np.array([x, y]),
                        (pix_square_size, pix_square_size)
                    )
                )

        if self.render_mode == "human":
            # the following line copies our drawings from 'canvas' to the visible window
            # self.window.blit(canvas, canvas.get_rect())
            self.window.blit(pygame.transform.flip(pygame.transform.rotate(canvas, 270), True, False), canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # we need to ensure that human-rendering occurs at the predefined framerate.
            # the following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])

            # save image
            pygame.image.save(self.window, "../captures/gridmaze.png")
        else: # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )
        

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from layouts import *

    layout = layout_8x8 # 8x8 grid
    env = GridMaze(layout, 100)
    obs, info = env.reset()

    frame = env.render("human")
    action = env.action_space.sample()
    n_obs, reward, done, info = env.step(action)

    env.close()