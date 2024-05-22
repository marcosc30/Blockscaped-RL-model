import tensorflow as tf
import numpy as np
import tf_agents
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.networks import q_network
from tf_agents.agents.dqn import dqn_agent
from tf_agents.utils import common
from gym_env import BlockscapeEnv

# Create a Gym environment
train_env = suite_gym.load(BlockscapeEnv)
eval_env = suite_gym.load(BlockscapeEnv)

# Wrap environments in TF environments
train_env = tf_py_environment.TFPyEnvironment(train_env)
eval_env = tf_py_environment.TFPyEnvironment(eval_env)

# Define Q-Network
fc_layer_params = (100,)
q_net = q_network.QNetwork(
    train_env.observation_spec(),
    train_env.action_spec(),
    fc_layer_params=fc_layer_params)

# Define DQN Agent
optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=1e-3)
train_step_counter = tf.Variable(0)
agent = dqn_agent.DqnAgent(
    train_env.time_step_spec(),
    train_env.action_spec(),
    q_network=q_net,
    optimizer=optimizer,
    td_errors_loss_fn=common.element_wise_squared_loss,
    train_step_counter=train_step_counter)

agent.initialize()


