import numpy as np
from blocks import main_block_list, print_block


# Default grid will be 8x8 and empty

default_grid = np.zeros((8, 8), dtype=int)

def pick_blocks_random():
    # define the blocks using 4 rotations of each type, then pick blocks from it
    # 1. pick 3 random types of block from main_block_list
    block_type = np.random.choice(main_block_list, 3)

    # 2. pick a random rotation of the block
    blocks = []
    for block in block_type:
        block_rotation = np.random.choice(block)
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

