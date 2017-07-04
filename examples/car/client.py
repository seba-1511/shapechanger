#!/usr/bin/env python

import gym
import mj_transfer
from mj_transfer.robots import NewBrightEnv

from time import time
import matplotlib.pyplot as plt
from scipy.misc import imshow, toimage, imsave

FREQUENCY = 0.25

try:
    # Windows
    from msvcrt import getch
except ImportError:
    # Unix
    import sys
    import tty
    import termios

    def getch():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

if __name__ == '__main__':
    env = gym.make('NewBright-v1')
    time_init = time()
    env.reset()
    while True:
        action = [0.0, 0.0, 0.0, 0.0]
        c = getch()
        if c == 'q':
            break
        if c == 'w':
            action[0] = 1.0
        if c == 's':
            action[1] = 1.0
        if c == 'd':
            action[2] = 1.0
        if c == 'a':
            action[3] = 1.0
        # TODO: Move the following code in env.step ?
        # TODO: Keep everything to 1.0 if key pressed ?
        # TODO: Deal with opposing directions ?
        env.step(action)
        # env.render()
    env.disconnect()
