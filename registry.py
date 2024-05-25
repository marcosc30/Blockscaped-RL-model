import gym
from gym.envs.registration import register

register(
    id='Blockscape-v0',
    entry_point='gym_env:BlockscapeEnv',
)