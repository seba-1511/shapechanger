
from time import sleep
from mj_transfer.robots import RemoteCatEnv

try:
    # Windows
    from msvcrt import getch
except ImportError:
    # Unix
    import sys
    import tty
    import termios

    def getch():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)



INIT_OFFSET = [0.0, 60.0, 30.0, 20.0, 0.0, 0.0, 20.0, 0.0, 0.0, 0.0, 60.0, 30.0]


def offset(action):
    return [o + a for o, a in zip(INIT_OFFSET, action)]


if __name__ == '__main__':
    env = RemoteCatEnv('192.168.42.1', 5000)

    env.reset()
    action = [0.0 for _ in range(12)]
    env.step(offset(action))
    sleep(0.5)

    for i in range(20):
        action = [0.0 for _ in range(12)]
        action = offset(action)
        _, r, _, _ = env.step(action)
        sleep(1.0)
        action[0] = 17.0
        action[1] = -52.0
        action[2] = -17.0
        action[3] = -17.0
        action[4] = 52.0
        action[5] = 17.0
        action[6] = -17.0
        action[7] = 52.0
        action[8] = 17.0
        action[9] = 17.0
        action[10] = -52.0
        action[11] = -17.0
        action = offset(action)
        _, r, _, _ = env.step(action)
        sleep(1.0)

    env.disconnect()
