import os, sys
import pickle
import pygame
import numpy as np
sys.path.append("/workspace/gridmaze")
from gridmaze.gridmaze import GridMaze
from gridmaze.layouts import *

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 127, 0)
ALPHA = 100

if __name__=="__main__":
    save_display = False

    # gridmaze environment
    layout = layout_8x8 # 8x8 grid
    env = GridMaze(layout, 100)
    env.reset()

    # pygame display setting
    text_field_size = 48
    fig_size = (env.window_size, env.window_size + text_field_size)
    display = pygame.display.set_mode(fig_size)
    display.fill(WHITE)
    pygame.display.set_caption("Generate Trajectory")

    frame_per_sec = pygame.time.Clock()
    fps = 4

    # font
    font = pygame.font.SysFont(None, 36)

    # event
    REACH_GOAL = pygame.USEREVENT + 1 # when agent reachs goal

    trajectories = [[]]
    ep = 0

    show_prev_traj = True

    running = True
    while running:
        # draw
        display.fill(WHITE)
        frame = env.render()
        surf = pygame.surfarray.make_surface(frame)
        text = font.render(f"Episode {ep},  Keys: Quit(q), Prev Traj(t)", True, BLACK)
        if show_prev_traj:
            pix_square_size = (env.window_size / env.grid_size[0])
            half_pix_square_size = pix_square_size // 2
            for j in range(len(trajectories)):
                for i in range(len(trajectories[j])):
                    (prev_x, prev_y) = trajectories[j][i][0] # obs
                    (x, y) = trajectories[j][i][2] # next_obs
                    pygame.draw.line(
                        surf,
                        pygame.Color(*ORANGE, ALPHA),
                        ((pix_square_size * prev_y) + half_pix_square_size, (pix_square_size * prev_x) + half_pix_square_size),
                        ((pix_square_size * y) + half_pix_square_size, (pix_square_size * x) + half_pix_square_size),
                        width=2,
                    )
        display.blit(text, (0, 0))
        display.blit(surf, (0, text_field_size))
        pygame.display.update()

        action = None

        # event handling
        for event in pygame.event.get():
            # quit the game
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                if save_display:
                    pygame.image.save(display, "../captures/gridmaze_traj.png")
                running = False

            # terminate episode
            if event.type == REACH_GOAL:
                trajectories.append([])
                env.reset()
                ep += 1

            # key pressed
            if event.type == pygame.KEYDOWN:
                # act
                if event.key == pygame.K_UP:
                    action = 0
                elif event.key == pygame.K_DOWN:
                    action = 1
                elif event.key == pygame.K_LEFT:
                    action = 2
                elif event.key == pygame.K_RIGHT:
                    action = 3
                # show previous trajectories
                elif event.key == pygame.K_t:
                    show_prev_traj = not show_prev_traj
        
        if action is not None:
            obs = env._get_obs()[0]
            next_obs, reward, done, _ = env.step(action)

            trajectories[ep].append((obs, action, next_obs[0], reward, done))

            # post event when the agent reaches the goal
            if done:
                pygame.event.post(pygame.event.Event(REACH_GOAL))

        frame_per_sec.tick(fps) # fps

    pygame.quit()
    print(trajectories)

    os.makedirs("../outputs", exist_ok=True)
    save_dir = "../outputs/trajectories.pickle"
    with open(save_dir, "wb") as f:
        pickle.dump(trajectories, f)