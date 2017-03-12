#!/usr/bin/env python

import gym
import mj_transfer

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
    while True:
        c = getch()
        if c == 'q':
            break
        action = [0, 0, 0, 0]
        if c == 'w':
            action[0] += 1.0
        if c == 's':
            action[1] += 1.0
        if c == 'd':
            action[2] += 1.0
        if c == 'a':
            action[3] += 1.0
        s = env.step(action)
        print(s)
