#!/usr/bin/env python

import time

from .remote_robot_env import RemoteRobotEnv


class NewBrightEnv(RemoteRobotEnv):

    def render(self):
        self.current_state.show()


if __name__ == '__main__':
    env = NewBrightEnv('192.168.42.1', 5000)

    env.reset()
    for _ in range(10):
        start = time.time()
        action = [0, 0, 1, 0]
        env.step(action)
        # env.render()
        print('Loop: ', time.time() - start)
    env.disconnect()
