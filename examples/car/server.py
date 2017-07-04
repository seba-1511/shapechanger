#!/usr/bin/env python

from mj_transfer.robots import NewBrightAgent, forever

if __name__ == '__main__':
    def main():
        robot = NewBrightAgent('192.168.42.1', 5000)
        try:
            robot.run()
            print('Run Finished')
        except:
            print('qwer')
            robot.clean()
        robot.clean()

    forever(main)
