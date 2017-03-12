#!/usr/bin/env python

import socket as sk
import struct as st

DEFAULT_PORT = 5000
DEFAULT_IP = '192.168.1.3'
# DEFAULT_IP = '127.0.0.1'
BUFFER_SIZE = 32


class RobotServer(object):
    def __init__(self):
        self.port = DEFAULT_PORT
        self.ip = DEFAULT_IP
        self.socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)
        conn, addr = self.socket.accept()
        print 'Address: ', addr
        self.conn = conn

    def recv(self):
        data = self.conn.recv(BUFFER_SIZE)
        data = st.unpack('ffff', data)
        return data

    def shutdown(self):
        self.conn.close()
