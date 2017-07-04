#!/usr/bin/env python

from gym.envs.registration import register

from .remote_robot_agent import RemoteRobotAgent
from .remote_robot_env import RemoteRobotEnv
from .new_bright_agent import NewBrightAgent
from .new_bright_env import NewBrightEnv

register(
    id='NewBright-v1',
    entry_point='mj_transfer:NewBrightEnv',
)
