# mj_transfer
Additional MuJoCo environments for OpenAI Gym

## Install Instructions

1. Clone this folder.
2. Simply execute `python setup.py develop ` in this folder.
3. You can now `import mj_transfer` to register them, and `gym.make('BigAnt-v1')` if you want to use the BigAnt env.

## Available Environments

### AmputedAnt-v1
Like Ant-v1, but with one-quarter leg missing. 

![](./web/figs/amputed_ant.png)

### BigAnt-v1
Like Ant-v1, but with long legs. 

![](./web/figs/big_ant.png)

### ExtendedAnt-v1
Like Ant-v1, but with an additional joint on each limb.

![](./web/figs/extended_ant.png)

### SmallInvertedPendulum-v1
Like InvertedPendulum, but with an arm half the size. 

![](./web/figs/small_inverted_pendulum.png)

### BigInvertedPendulum-v1
Like InvertedPendulum, but with an arm twice the size. 

![](./web/figs/big_inverted_pendulum.png)

### Finger-v1
A realistic tendon-driven finger.

![](./web/figs/finger.png)

# MuJoCo Tutorial
You can find a short tutorial for that explains the basics of MuJoCo there: [seba-1511.github.io/mj_transfer](seba-1511.github.io/mj_transfer)
