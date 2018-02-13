
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



# INIT_OFFSET = [0.0, 60.0, 30.0, 20.0, 0.0, 0.0, 20.0, 0.0, 0.0, 0.0, 60.0, 30.0]
INIT_OFFSET = [55.0, 92.0, 55.0]
INIT_OFFSET = INIT_OFFSET * 4


def offset(action):
    return [o + a for o, a in zip(INIT_OFFSET, action)]


def stand(action):
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
    return action


def lie(action):
    return offset(action)


def flex_front(action):
    action[0] = 17.0
    action[1] = -52.0
    action[2] = -17.0
    action[3] = -17.0
    action[4] = 52.0
    action[5] = 17.0
    return offset(action)


def flex_back(action):
    action[6] = -17.0
    action[7] = 52.0
    action[8] = 17.0
    action[9] = 17.0
    action[10] = -52.0
    action[11] = -17.0
    return offset(action)


if __name__ == '__main__':
    env = RemoteCatEnv('192.168.42.1', 5000)

    env.reset()
    action = [0.0 for _ in range(12)]
    env.step(offset(action))
    sleep(0.5)

    while True:
        print('Action:')
        c = getch()
        action = [0.0 for _ in range(12)]
        if c == 'l':
            action = lie(action)
        elif c == 'f':
            action = flex_front(action)
        elif c == 'b':
            action = flex_back(action)
        elif c == 's':
            action = stand(action)
        elif c == 'q':
            print('Quit')
            env.disconnect()
            quit()
        env.step(action)

    env.disconnect()
