import gym
from gym import spaces


class BlockscapeEnv(gym.Env):
    def __init__(self):
        super(BlockscapeEnv, self).__init__()

        # Define action and observation space
        # They must be gym.spaces objects
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Discrete(1)

    def step(self, action):
        # Execute one time step within the environment
        if action == 0:
            return 0, 1, True, {}
        else:
            return 0, 0, True, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        return 0

    def render(self, mode='human'):
        # Render the environment to the screen
        pass

# Test the environment
env = CustomEnv()
print(env.action_space.sample())
print(env.step(0))


def main():
    env = gym.make('CartPole-v1')  # Create the environment
    env.reset()  # Reset the environment to start

    for _ in range(1000):  # Run for a certain number of steps
        env.render()  # Render the environment to the screen

        action = env.action_space.sample()  # Select a random action
        observation, reward, done, info = env.step(action)  # Take a step in the environment with the selected action

        if done:  # If the environment says the game is done, reset it for the next run
            env.reset()

    env.close()  # Close the environment

if __name__ == "__main__":
    main()