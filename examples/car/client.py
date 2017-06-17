#!/usr/bin/env python

import gym
import mj_transfer

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
    action = [0.0, 0.0, 0.0, 0.0]
    while True:
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
        if time() - time_init > FREQUENCY:
            s_a = sum(action)
            if not s_a == 0:
                print(action)
                s = env.step(action)
                # import pdb; pdb.set_trace()
                # imsave('./feed.jpg', s)
                # plt.imshow(toimage(s))
                # toimage(s).show()
            action = [0.0, 0.0, 0.0, 0.0]
            time_init = time()
