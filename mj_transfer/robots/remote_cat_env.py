#!/usr/bin/env python

import time
import struct as st

from .remote_robot_env import RemoteRobotEnv


class RemoteCatEnv(RemoteRobotEnv):

    def _wait_first_state(self):
        state = self.recv()
        self.current_state = state[1:]

    def step(self, action):
        self.send(action)
        state = self.recv()
        reward, state = state[0], state[1:]
        self.current_state = state
        return state, reward, False, {}

    def recv(self):
        data = self.socket.recv(52)
        data = st.unpack('fffffffffffff', data)
        return data

    def render(self):
        print(self.current_state)

    def disconnect(self):
        self.send([-1 for _ in range(12)])


if __name__ == '__main__':
    env = RemoteCatEnv('192.168.42.1', 5000)

    env.reset()
    for _ in range(10):
        start = time.time()
        action = [1.0 for _ in range(12)]
        env.step(action)
        time.sleep(1)
        action = [a*90 for a in action]
        env.step(action)
    env.disconnect()
