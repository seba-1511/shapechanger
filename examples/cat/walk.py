
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



INIT_OFFSET = [55.0, 92.0, 55.0]
INIT_OFFSET = INIT_OFFSET * 4


def offset(action):
    return [o + a for o, a in zip(INIT_OFFSET, action)]


# WALK_CYCLE = [
        # [9.6   , -31.06 , -10.73 , -9.6   , 31.06 , 10.73 , -9.39 , 27.96 , 9.29  , 9.39  , -27.96 , -9.29]  ,
        # [-0.11 , -0.11  , -0.11  , 0.11   , 0.11  , 0.11  , 0.11  , 0.11  , 0.11  , -0.11 , -0.11  , -0.11]  ,
        # [10.42 , -10.42 , 0.00   , -10.42 , 10.42 , 0.00  , 5.47  , 5.47  , 5.47  , -5.47 , -5.47  , -5.47]  ,
        # [19.39 , -34.25 , -7.43  , -19.39 , 34.25 , 7.43  , -0.16 , 30.7  , 15.27 , 0.16  , -30.7  , -15.27] ,
        # [10.74 , -34.46 , -11.86 , -10.74 , 34.46 , 11.86 , -7.12 , 25.69 , 9.29  , 7.12  , -25.69 , -9.29]  ,
    # ]

WALK_CYCLE = [
        [19.39 , -34.25 , -7.43  , -9.6   , 31.06 , 10.73 , -9.39 , 27.96 , 9.29  , 0.16  , -30.7  , -15.27]  ,
        [10.74 , -34.46 , -11.86 , 0.11   , 0.11  , 0.11  , 0.11  , 0.11  , 0.11  , 7.12  , -25.69 , -9.29]  ,
        [9.6   , -31.06 , -10.73 , -10.42 , 10.42 , 0.00  , 5.47  , 5.47  , 5.47  , 9.39  , -27.96 , -9.29]  ,
        [-0.11 , -0.11  , -0.11  , -19.39 , 34.25 , 7.43  , -0.16 , 30.7  , 15.27 , -0.11 , -0.11  , -0.11] ,
        [10.42 , -10.42 , 0.00   , -10.74 , 34.46 , 11.86 , -7.12 , 25.69 , 9.29  , -5.47 , -5.47  , -5.47]  ,
                                                               


    ]



def dephase(step):
    off = -1
    action = list(WALK_CYCLE[step])
    # action[3:6] = WALK_CYCLE[(step+off)%len(WALK_CYCLE)][3:6]
    # action[6:9] = WALK_CYCLE[(step+off)%len(WALK_CYCLE)][6:9]
    action = offset(action)
    action = [int(a) for a in action]
    return action


if __name__ == '__main__':
    env = RemoteCatEnv('192.168.42.1', 5000)

    env.reset()
    action = [0.0 for _ in range(12)]
    env.step(offset(action))
    sleep(00.5)

    action = INIT_OFFSET
    env.step(action)
    # sleep(1000)
    reward = 0.0
    for _ in range(10):
        for i in range(len(WALK_CYCLE)):
            action = dephase(i)
            for a in action:
                if a > 170 or a < 0: print('problem')
            s, r, _, _ = env.step(action)
            reward += r
            print('step reward: ', r)
            # sleep(1)
    print('Total reward: ', reward)

    env.disconnect()
