#!/usr/bin/env python

import io
import time
import socket as sk
import struct as st
from PIL import Image

# The class below essentially implements those lines, but fitting the OpenAI Gym
# environment structure.
# socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
# socket.connect(('127.0.0.1', 5000))

# def predictor_process(make_prediction=None):
    # if make_prediction is None:
        # make_prediction = lambda s, r: [0, 1, 0, 0]
    # while True:
        # data = socket.recv(32)
        # state = st.unpack('ffff', data)
        # reward, state = state[0], state[1:]
        # print('Received state: ', state)
        # print('Predicting...')
        # action = make_prediction(state, reward)
        # msg = st.pack('f'*len(action), *action)
        # print('Sending action')
        # socket.send(msg)


class RemoteRobotEnv(object):

    """
    This interface for remote robots executes the following:
        1. Init the socket connection
        2. While True:
            a. recv(state, reward)
            b. process
            c. send(action)
    But it has been slightly re-written, to accomodate for a more flexible 
    robotical interface.
    """

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        # Receive the initial state
        self._wait_first_state()

    def _wait_first_state(self):
        reward = self.recv()
        reward, state_size = reward[0], reward[1]
        state = self.recv_image(state_size)
        self.current_state = state

    def recv_image(self, img_size):
        img = ''
        while len(img) < img_size:
            img += self.socket.recv(2048)
        img = Image.open(io.BytesIO(img))
        return img

    def send(self, msg):
        msg = st.pack('f'*len(msg), *msg)
        self.socket.send(msg)

    def recv(self):
        data = self.socket.recv(32)
        data = st.unpack('ffff', data)
        return data

    def reset(self):
        return self.current_state

    def step(self, action):
        self.send(action)
        reward = self.recv()
        reward, state_size = reward[0], reward[1]
        state = self.recv_image(state_size)
        self.current_state = state
        return state, reward, False, {}

    def disconnect(self):
        self.send([-1, -1, -1, -1])

    # Overrideable
    def render(self):
        pass


if __name__ == '__main__':
    env = RemoteRobotEnv('192.168.42.1', 5000)

    env.reset()
    for _ in range(10):
        start = time.time()
        action = [0, 0, 1, 0]
        env.step(action)
        print('Loop: ', time.time() - start)
    env.disconnect()
