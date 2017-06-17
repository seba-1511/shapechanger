#!/usr/bin/env python

import numpy as np
import gym
import mj_transfer
import sys
from time import sleep

# Should be a custom env
# ENV = 'SmallInvertedPendulum-v1'
# ENV = 'BigInvertedPendulum-v1'
# ENV = 'AmputedAnt-v1'
# ENV = 'BigAnt-v1'
# ENV = 'ExtendedAnt-v1'
ENV = 'Finger-v1'


if __name__ == '__main__':
    env = gym.make(ENV)
    for i in xrange(15):
        s = env.reset()
        a = np.array([0, 0, 0, 0, 0, 0, 0], dtype=np.float32)
        while True:
            a = (np.random.rand(*env.action_space.shape) - 0.5) * 1.1
            s, r, d, _ = env.step(a)
            # print('Reward: ', r)
            env.render()
            # sleep(0.1)
            # a += 0.1
            if d: 
                break
        
