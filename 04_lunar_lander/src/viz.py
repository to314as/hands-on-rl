from time import sleep
from argparse import ArgumentParser
from pdb import set_trace as stop
from typing import Optional

import pandas as pd
import gymnasium as gym

from src.config import SAVED_AGENTS_DIR

import numpy as np

def make_video(agent):

    import gymnasium as gym
    from gymnasium.wrappers import Monitor
    env = Monitor(gym.make('CartPole-v1'), './video', force=True)

    state, _ = env.reset()
    done = False

    while not done:
        # action = env.action_space.sample()
        import torch
        action = agent.act(torch.as_tensor(state, dtype=torch.float32))
        state_next, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
    env.close()


def show_video(
    agent,
    env,
    sleep_sec: float = 0.1,
    seed: Optional[int] = 0,
    mode="rgb_array",
):

    try:
        state, _ = env.reset(seed)
    except TypeError:
        print("Warning: Seed not supported by environment")
        state, _ = env.reset()

    # LAPADULA
    if mode == "rgb_array":
        from matplotlib import pyplot as plt
        from IPython.display import display, clear_output
        steps = 0
        fig, ax = plt.subplots(figsize=(8, 6))

    terminated = False
    truncated = False
    while not (terminated or truncated):

        import torch
        action = agent.act(torch.as_tensor(state, dtype=torch.float32))

        state, reward, terminated, truncated, info = env.step(action)

        # LAPADULA
        if mode == "rgb_array":
            steps += 1
            frame = env.render()
            ax.cla()
            ax.axes.yaxis.set_visible(False)
            ax.imshow(frame)
            ax.set_title(f'Steps: {steps}')
            display(fig)
            clear_output(wait=True)
            plt.pause(sleep_sec)
        else:
            env.render()
            sleep(sleep_sec)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--agent_id', type=str, required=True)
    parser.add_argument('--sleep_sec', type=float, required=False, default=0.1)
    args = parser.parse_args()

    from src.base_agent import BaseAgent
    agent_path = SAVED_AGENTS_DIR / args.agent_file
    agent = BaseAgent.load_from_disk(agent_path)

    from src.q_agent import QAgent

    env = gym.make('CartPole-v1', render_mode="rgb_array")
    # env._max_episode_steps = 1000

    show_video(agent, env, sleep_sec=args.sleep_sec)








