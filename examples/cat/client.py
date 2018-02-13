
import time

from mj_transfer.robots import RemoteCatEnv

if __name__ == '__main__':
    env = RemoteCatEnv('192.168.42.1', 5000)

    env.reset()
    action = [0.0 for _ in range(12)]
    pin = 0
    for _ in range(10):
        start = time.time()
        action = [1.0 for _ in range(12)]
        # action[pin] = 90
        _, r, _, _ = env.step(action)
        print('reward: ', r)
        action = [a*180 for a in action]
        # action[pin] = 0
        env.step(action)
        print('loop: ', time.time() - start)
        # time.sleep(0.66)
    env.disconnect()
