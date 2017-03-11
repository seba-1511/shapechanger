#!/usr/bin/env python

from mj_transfer.robotics import RobotServer

if __name__ == '__main__':
    master = RobotServer()
    try:
        for i in xrange(10):
            data = master.recv()
            print data
    except Exception as e:
        master.shutdown()
        print e
