#!/usr/bin/env python

import socket as sk
import struct as st
import numpy as np

try:
    from cStringIO import StringIO
except:
    from io import StringIO


from .robot_server import DEFAULT_PORT, DEFAULT_IP


class NewBrightEnv(object):
    def __init__(self):
        self.server_ip = DEFAULT_IP
        self.server_port = DEFAULT_PORT
        self.socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.socket.connect((self.server_ip, self.server_port))

    def set_server_ip(self, ip):
        self.server_ip = ip

    def step(self, action):
        """
        action is an iterable similar to [f, b, l, r] where:
        f: amount to go forward (0-1),
        b: amount to go backward (0-1),
        l: amount to go left (0-1),
        r: amount to go right (0-1).
        """
        assert(len(action) == 4)
        action = [min(max(0.0, a), 1.0) for a in action]
        msg = st.pack('f'*len(action), *action)
        self.socket.send(msg)
        img = self.recv_image()
        return img

    def recv_image(self):
        img_size = self.socket.recv(8)
        img_size = int(img_size)
        ultimate_buffer = ''
        while len(ultimate_buffer) < img_size:
            receiving_buffer = self.socket.recv(2048)
            # if not receiving_buffer: break
            ultimate_buffer += receiving_buffer
            print('-',)
        print('')
        final_image = np.load(StringIO(ultimate_buffer))['frame']
        # final_image = np.fromstring(ultimate_buffer)
        return final_image
        return [0, 0]

    def reset(self):
        pass

    def render(self):
        pass

