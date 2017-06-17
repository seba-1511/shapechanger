#!/usr/bin/env python

from .new_bright import NewBrightEnv
from .robot_server import RobotServer

try:
    from gym.envs.registration import register

    register(
        id='NewBright-v1',
        entry_point='mj_transfer:NewBrightEnv',
    )
except:
    print('OpenAI Gym not installed')
