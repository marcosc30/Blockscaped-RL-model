import gym
from gym import spaces
from blocks import main_block_list
from game import print_grid, pick_blocks_random, pick_blocks_custom, print_block, is_allowed, place_block, is_possible, update_grid, default_grid
import numpy as np


def block_to_int(block):
    # This could be done more efficiently with a dictionary, but this is a simple way to convert a block to a discrete integer
    i = 1
    for block in main_block_list:
        for rotation in block:
            if block == block:
                return i
            i += 1

def int_to_block(int):
    # Turns a discrete integer into a block 
    i = 1
    for block in main_block_list:
        for rotation in block:
            if i == int:
                return rotation
            i += 1

def grid_to_binarray(grid):
    # Turns a grid into a binary array
    grid = grid.flatten()
    return grid

class BlockscapeEnv(gym.Env):
    def __init__(self):
        super(BlockscapeEnv, self).__init__()

        # Define action and observation space
        # They must be gym.spaces objects

        possible_blocks = 1 # 1 for an empty block, we will make it so a block is replaced by the empty block when used
        for block_rotations in main_block_list:
            possible_blocks += len(block_rotations)
        # if the model tries to use the empty block, it will just step forward into the same situation

        # three shapes to pick from, 64 possible placement values
        self.action_space = spaces.MultiDiscrete([3, 64])
        self.observation_space = spaces.Tuple(
            [spaces.MultiDiscrete([possible_blocks, possible_blocks, possible_blocks]), # Available blocks
            spaces.MultiBinary(64)]) # Grid
            #spaces.Box(low=0, high=float('inf'), shape=(1,), dtype=np.float32)]) # Score
        
        # state variables
        self.score = 0
        self.current_steps = 0
        self.max_steps = 2000

    def get_block(self):
        # This returns the current 3 blocks, in block form
        blocks = self.observation_space[0]
        block_forms = []
        for block in blocks:
            block_forms.append(int_to_block(block))
        return block_forms

    def get_grid(self):
        # This returns the current grid
        grid = np.array(self.observation_space[1])
        grid = grid.reshape((8, 8))
        return grid

    def step(self, action):
        # Execute one time step within the environment
        # Returns (observation, reward, done, info)
        # 1. If all blocks are empty in the observation space, we pick 3 new blocks and place them in the observation space then finish the step
        if np.array_equal(self.observation_space[0], np.zeros(3)):
            random_blocks = pick_blocks_random()
            block_ints = []
            for block in random_blocks:
                block_ints.append(block_to_int(block))
            new_observation_space = block_ints, self.observation_space[1]#, self.observation_space[2]
            self.observation_space = new_observation_space
            return self.observation_space, 0, False, {}

        # 2. If the action is to place an empty block, we just step forward, detracting a small amount from the reward to guide it not to do this
        if self.observation_space[0][action[0]] == 0:
            #print("0 action")
            return self.observation_space, -10, False, {}
        
        # 3. Get the blocks and grid to make working with it easier
        blocks = self.get_block()
        grid = self.get_grid()

        nones_removed = blocks.copy()
        for block in blocks:
            if block is None:
                nones_removed.remove(block)
        
        # 3. If none of the blocks are placeable, we end the game
        if not any([is_possible(grid, block) for block in nones_removed]):
            print("Game Over")
            print("Score: ", self.score)
            return self.observation_space, 0, True, {}

        # 4. If the action is to place a block, we check if the block can be placed and place it if it can, otherwise we step forward without doing anything
        block = blocks[action[0]]
        x = action[1] // 8
        y = action[1] % 8
        if is_allowed(grid, block, x, y):
            #print("real action")
            placed_grid = place_block(grid, block, x, y)
            new_grid, round_score = update_grid(placed_grid, self.score, block)
            round_score = round_score - self.score
            self.score += round_score

            # We update the blocks, grid and score
            self.observation_space[0][action[0]] = 0
            new_observation_space = self.observation_space[0], grid_to_binarray(new_grid)#, self.score
            self.observation_space = new_observation_space
        else:
            # This loss is to encourage it to not get into an infinite loop of trying to place a block that can't be placed
            round_score = -10
        return self.observation_space, round_score, False, {}


    def reset(self):
        # Reset the state of the environment to an initial state
        self.score = 0
        self.current_steps = 0
        self.observation_space = (np.zeros(3), np.zeros(64))#, np.zeros(1))

        return self.observation_space, self.score, False, {}

    # def render(self, mode='human'):
    #     # Render the environment to the screen
    #     print_grid(self.observation_space[1])

