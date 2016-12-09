import numpy as np
from gym import utils
from gym.envs.mujoco import mujoco_env
import os

class FingerEnv(mujoco_env.MujocoEnv, utils.EzPickle):
    def __init__(self):
        env_file = os.path.dirname(__file__) + '/assets/finger.xml'
        utils.EzPickle.__init__(self)
        mujoco_env.MujocoEnv.__init__(self, env_file, 2)

    def _step(self, a):
        vec = self.get_body_com("fingertip")-self.get_body_com("target")
        reward_dist = - np.linalg.norm(vec)
        # reward_ctrl = - np.square(a).sum()
        reward_ctrl = 0.0
        reward = reward_dist + reward_ctrl
        self.do_simulation(a, self.frame_skip)
        ob = self._get_obs()
        # done = False
        done = reward_dist > -0.2
        return ob, reward, done, dict(reward_dist=reward_dist, reward_ctrl=reward_ctrl)

    def viewer_setup(self):
        self.viewer.cam.trackbodyid=2

    def reset_model(self):
        # TODO: It might be a good idea to re-introduce noise once later.
        # qpos = self.np_random.uniform(low=-0.1, high=0.1, size=self.model.nq) + self.init_qpos
        qpos = self.init_qpos
        while True:
            self.goal = (self.np_random.uniform(low=-1.5, high=-0.5, size=1),
                         self.np_random.uniform(low=-0.3, high=0.3, size=1),
                         self.np_random.uniform(low=-1.8, high=0.1, size=1))
            if np.linalg.norm(self.goal) < 2: break
        qpos[-3:] = self.goal
        # qpos[-2:] = self.goal
        # qvel = self.init_qvel + self.np_random.uniform(low=-.005, high=.005, size=self.model.nv)
        qvel = 0.0*self.init_qvel
        qvel[-3:] = 0
        # qvel[-2:] = 0
        self.set_state(qpos, qvel)
        return self._get_obs()

    def _get_obs(self):
        theta = self.model.data.qpos.flat[:2]
        return np.concatenate([
            np.cos(theta),
            np.sin(theta),
            self.model.data.qpos.flat[2:],
            self.model.data.qvel.flat[:2],
            self.get_body_com("fingertip") - self.get_body_com("target")
        ])
