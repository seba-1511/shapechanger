#!/usr/bin/env python

import gym
import mj_transfer
from mj_transfer.robots import NewBrightEnv

from time import time, sleep
import matplotlib.pyplot as plt
from scipy.misc import imshow, toimage, imsave

import torch as th
from torch.autograd import Variable as V
from torchvision import transforms
from train import DrivingNet

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
    env = NewBrightEnv('192.168.42.1', 5000)
    time_init = time()
    model = DrivingNet()
    model.load_state_dict(th.load('./model.pth'))
    transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.25, 0.25, 0.25]),
        ])
    state = env.reset()
    while True:
        action = [0.0, 0.0, 0.0, 0.0]
        # print('waiting for action')
        # c = getch()
        c = None
        sleep(0.7)
        if c == 'q':
            break
        
        start = time()
        state = state.convert('RGB')
        state = V(transform(state))
        action = model(state.view(1, state.size(0), state.size(1), state.size(2)))
        action = action.data.tolist()[0]
        print(action)
        action = [1.0 if a > 0.2 else 0.0 for a in action]

        # TODO: Move the following code in env.step ?
        # TODO: Keep everything to 1.0 if key pressed ?
        # TODO: Deal with opposing directions ?
        state, reward, done, info = env.step(action)
        # env.render()
    env.disconnect()
