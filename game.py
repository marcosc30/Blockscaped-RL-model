import numpy as np
from blocks import main_block_list, print_block
import random


# Default grid will be 8x8 and empty

default_grid = np.zeros((8, 8), dtype=int)

def pick_blocks_random():
    # define the blocks using 4 rotations of each type, then pick blocks from it
    # 1. pick 3 random types of block from main_block_list
    original_list = main_block_list.copy()
    block_type_1 = random.choice(original_list)
    original_list.remove(block_type_1)
    block_type_2 = random.choice(original_list)
    original_list.remove(block_type_2)
    block_type_3 = random.choice(original_list)
    block_types = [block_type_1, block_type_2, block_type_3]

    # 2. pick a random rotation of the block
    blocks = []
    for block in block_types:
        block_rotation = random.choice(block)
        blocks.append(block_rotation)

    return blocks

def pick_blocks_custom():
    # define the blocks using 4 rotations of each type, then pick blocks from it
    # 1. print all of the block options
    block_index = 1
    for block in main_block_list:
        print("Block type: ", block_index)
        print_block(block[0])
        print("\n")
        block_index += 1
    
    # 2. pick 3 types of block from main_block_list based on user inputs
    block_type = []
    for i in range(3):
        done_with_this_block = False
        while not done_with_this_block:
            u_input = int(input("Enter block type: ")) - 1
            if u_input >= 0 and u_input < len(main_block_list):
                block_type.append(main_block_list[u_input])
                done_with_this_block = True
            else:
                print("Invalid block type. Please try again.")

    # 3. print rotations of each block            

    # 4. pick rotations for each block
    block_index = 1
    blocks = []
    for block in block_type:
        # print all rotations of the block
        print("Pick Rotation For Block ", block_index)
        block_index += 1
        rotation_index = 1
        for rotation in block:
            print("Rotation: ", rotation_index)
            print_block(rotation)
            print("\n")
            rotation_index += 1 

        # pick a rotation
        done_with_this_block = False
        while not done_with_this_block:
            u_input = int(input("Enter block rotation: ")) - 1
            if u_input >= 0 and u_input < len(block):
                blocks.append(block[u_input])
                done_with_this_block = True
            else:
                print("Invalid block rotation. Please try again.")

    return blocks

def is_allowed(grid, block, x, y):
    # Function to check if a block can be placed at a certain position on the grid
    # 1. Find the dimensions of the block
    max_x = 0
    max_y = 0
    for cell in block:
        if cell[0] > max_y:
            max_y = cell[0]
        if cell[1] > max_x:
            max_x = cell[1]
    
    # 2. Check if the block can be placed at the given position
    for cell in block:
        if x + cell[0] >= grid.shape[0] or y + cell[1] >= grid.shape[1]:
            return False
        if grid[x + cell[0], y + cell[1]] == 1:
            return False
    return True

def place_block(grid, block, x, y):
    # Function to place a block on the grid
    assert(is_allowed(grid, block, x, y))
    for cell in block:
        grid[x + cell[0], y + cell[1]] = 1
    return grid


def print_grid(grid):
    # Function to print the grid into the console
    for row in grid:
        for cell in row:
            if cell == 1:
                print("██", end="")
            else:
                print("  ", end="")
        print("")

def update_grid(grid, score, last_block):
    # Check for how many rows are full
    full_rows = []
    for i in range(grid.shape[0]):
        if np.all(grid[i, :] == 1):
            full_rows.append(i)
    
    # Check for how many columns are full
    full_columns = []
    for i in range(grid.shape[1]):
        if np.all(grid[:, i] == 1):
            full_columns.append(i)
    
    # Make the full columns and rows empty
    for row in full_rows:
        grid[row, :] = 0
    for column in full_columns:
        grid[:, column] = 0
    
    # Update the score
    lines_cleared = len(full_rows) + len(full_columns)
    grid_length = grid.shape[0]
    # grid_length should be 8 for default grid, this score calculation wouldn't work for non-square grids but I generalized it to all square sizes
    assert(grid_length == 8)
    block_size = len(last_block)
    score_increase = 0
    if lines_cleared == 0 or lines_cleared == 1:
        score_increase = (block_size + lines_cleared * grid_length)
    else:
        score_increase = (block_size + lines_cleared * grid_length) * lines_cleared
    score += score_increase

    return grid, score

def is_possible(grid, block):
    # check if block can be placed anywhere on the grid
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if is_allowed(grid, block, i, j):
                return True

def play_game():
    # Function to play the game
    # 1. Initialize the grid and score
    grid = default_grid
    score = 0
    game_is_over = False

    # 2. Play the game
    while not game_is_over:
        # 2.1. Pick a random block
        blocks = pick_blocks_random()
        round_is_over = False
        while not round_is_over:
            # 2.2. Check if the game is over
            if not any([is_possible(grid, block) for block in blocks]):
                print("Game Over!")
                game_is_over = True
                break

            # To make faster, this should be a subloops so we aren't checking for possible every time an input is not allowed
            subround_is_over = False
            while not subround_is_over:
                # 2.3. Print the grid
                print_grid(grid)
                print("Score: ", score)

                # 2.4. Print the blocks
                print("Next Blocks:")
                for block in blocks:
                    print_block(block)
                    print("\n")

                # 2.5. Ask the user for input
                block = blocks[int(input("Enter block number: ")) - 1]
                x = int(input("Enter x coordinate: "))
                y = int(input("Enter y coordinate: "))

                # 2.6. Place the block on the grid
                if not is_allowed(grid, block, x, y):
                    print("Block cannot be placed at this position. Try again.")
                    continue
                else:
                    grid = place_block(grid, block, x, y)
                    grid, score = update_grid(grid, score, block)
                    blocks.remove(block)
                    subround_is_over = True
                if blocks == []:
                    subround_is_over = True
                    round_is_over = True
