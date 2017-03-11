#!/usr/bin/env python

import gym
import mj_transfer

if __name__ == '__main__':
    env = gym.make('NewBright-v1')
    while True:
        c = raw_input('Command: ')
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
