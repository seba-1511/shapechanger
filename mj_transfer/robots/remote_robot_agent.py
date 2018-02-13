#!/usr/bin/env python

import socket as sk
import struct as st

BUFFER_SIZE = 16


class RemoteRobotAgent(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
        socket.bind((self.ip, self.port))
        print('Waiting for connection')
        socket.listen(1)
        conn, address = socket.accept()
        self.conn = conn
        self.socket = socket
        self.cleaned = False

    def send(self, msg):
        msg = st.pack('f'*len(msg), *msg)
        self.conn.send(msg)

    def recv(self):
        data = self.conn.recv(BUFFER_SIZE)
        data = st.unpack('ffff', data)
        return data

    def clean(self):
        if not self.cleaned:
            self.conn.shutdown(sk.SHUT_RDWR)
            self.conn.close()
            self.socket.shutdown(sk.SHUT_RDWR)
            self.socket.close()
            self.cleaned = True

    # Overrideable
    def run(self):
        pass

def forever(fn):
    while True:
        try:
            fn()
        except Exception:
            pass
            # print(str(e))

def main():
    robot = RemoteRobot('192.168.42.1', 5000)
    try:
        robot.run()
        print('Run Finished')
    except:
        print('qwer')
        robot.clean()
    robot.clean()


if __name__ == '__main__':
    # main()
    forever(main)
