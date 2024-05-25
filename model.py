import gym
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
import registry
from collections import deque

# Initialize the environment
env = gym.make('Blockscape-v0')

def preprocess_state(state):
    multi_discrete_part, multi_binary_part = state
    multi_discrete_part = torch.tensor(multi_discrete_part, dtype=torch.float32)
    multi_binary_part = torch.tensor(multi_binary_part, dtype=torch.float32)
    #box_part = torch.tensor(box_part, dtype=torch.float32)
    return torch.cat((multi_discrete_part.flatten(), multi_binary_part)).unsqueeze(0)


class QNetwork(nn.Module):
    def __init__(self, input_size, action_size):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, 1000)
        self.fc2 = nn.Linear(1000, 250)
        self.fc3 = nn.Linear(250, action_size)

    def forward(self, state):
        x = torch.relu(self.fc1(state))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# Calculate the input size based on the observation space
multi_discrete_size = env.observation_space[0].nvec.size
multi_binary_size = env.observation_space[1].n
input_size = multi_discrete_size + multi_binary_size
action_size = np.prod(env.action_space.nvec)  # Total number of actions

class ReplayMemory:
    def __init__(self, capacity):
        self.memory = deque(maxlen=capacity)

    def push(self, transition):
        self.memory.append(transition)

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
    

def train_dqn(env, num_episodes, gamma=0.99, epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995, batch_size=64, replay_memory_capacity=10000, lr=0.001):
    state_size = input_size
    action_size = np.prod(env.action_space.nvec)

    q_network = QNetwork(state_size, action_size)
    target_network = QNetwork(state_size, action_size)
    target_network.load_state_dict(q_network.state_dict())
    target_network.eval()

    optimizer = optim.Adam(q_network.parameters(), lr=lr)
    memory = ReplayMemory(replay_memory_capacity)

    epsilon = epsilon_start

    for episode in range(num_episodes):
        raw_state = env.reset()
        observation_state = preprocess_state(raw_state[0])
        state = observation_state#, raw_state[1], raw_state[2], raw_state[3]
        total_reward = 0

        for t in range(1000):
            if random.random() < epsilon:
                action = np.random.randint(0, action_size)  # Random action from the MultiDiscrete space
            else:
                with torch.no_grad():
                    action = q_network(state).max(1)[1].item()

            # Convert action index back to tuple form
            action_tuple = np.unravel_index(action, env.action_space.nvec)
            next_state, reward, done, _ = env.step(action_tuple)
            next_state = preprocess_state(next_state)
            memory.push((state, action, reward, next_state, done))

            state = next_state
            total_reward += reward

            if done:
                break

            if len(memory) > batch_size:
                transitions = memory.sample(batch_size)
                batch_state, batch_action, batch_reward, batch_next_state, batch_done = zip(*transitions)

                batch_state = torch.cat(batch_state)
                batch_action = torch.tensor(batch_action).unsqueeze(1)
                batch_reward = torch.tensor(batch_reward).unsqueeze(1)
                batch_next_state = torch.cat(batch_next_state)
                batch_done = torch.tensor(batch_done).unsqueeze(1).float()

                current_q_values = q_network(batch_state).gather(1, batch_action)
                next_max_q_values = target_network(batch_next_state).max(1)[0].detach().unsqueeze(1)
                expected_q_values = batch_reward + (gamma * next_max_q_values * (1 - batch_done))

                loss = nn.MSELoss()(current_q_values, expected_q_values)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            if t % 10 == 0:
                target_network.load_state_dict(q_network.state_dict())

        epsilon = max(epsilon_end, epsilon_decay * epsilon)
        print(f"Episode {episode+1}, Total Reward: {total_reward}, Epsilon: {epsilon:.2f}")

train_dqn(env, num_episodes=500)
