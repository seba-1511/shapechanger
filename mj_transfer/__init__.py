from gym.envs.registration import register

from .amputed_ant import AmputedAntEnv
from .big_ant import BigAntEnv
from .small_inverted_pendulum import SmallInvertedPendulumEnv
from .big_inverted_pendulum import BigInvertedPendulumEnv
from .extended_ant import ExtendedAntEnv

register(
    id='AmputedAnt-v1',
    entry_point='mj_transfer:AmputedAntEnv',
)

register(
    id='BigAnt-v1',
    entry_point='mj_transfer:BigAntEnv',
)

register(
    id='SmallInvertedPendulum-v1',
    entry_point='mj_transfer:SmallInvertedPendulumEnv',
)

register(
    id='BigInvertedPendulum-v1',
    entry_point='mj_transfer:BigInvertedPendulumEnv',
)

register(
    id='ExtendedAnt-v1',
    entry_point='mj_transfer:ExtendedAntEnv',
)
