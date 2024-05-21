import numpy as np

# Here, we define all of the types of blocks

# A block definition is a list of relative indices, starting from (0,0) which is the top leftmost cell of the block
# If there is no top leftmost cell objectively, then (0,0) is the cell with the x of the left most block and the y of the topmost block, 
# It is just not included in the cell

# Rotations are in order of rightwards 90 degree rotation

# L_left:
# 1
# 1
# 1 1
L_left_rotation_0 = [(0, 0), (0, 1), (0, 2), (1, 0)]
L_left_rotation_1 = [(0, 0), (0, 1), (1, 1), (2, 1)]
# This one is complicated so we will write it
# 1 1
# 0 1
# 0 1
L_left_rotation_2 = [(1, 0), (1, 1), (1, 2), (0, 2)]
L_left_rotation_3 = [(0, 0), (1, 0), (2, 0), (2, 1)]

L_left = [L_left_rotation_0, L_left_rotation_1, L_left_rotation_2, L_left_rotation_3]

# L_right:
#   1
#   1
# 1 1
L_right_rotation_0 = [(0, 0), (1, 0), (1, 1), (1, 2)]
L_right_rotation_1 = [(0, 0), (0, 1), (1, 0), (2, 0)]
L_right_rotation_2 = [(0, 0), (0, 1), (0, 2), (1, 2)]
# This one is complicated so we will write it
# 1 1 1
# 0 0 1
L_right_rotation_3 = [(0, 1), (1, 1), (2, 1), (2, 0)]

L_right = [L_right_rotation_0, L_right_rotation_1, L_right_rotation_2, L_right_rotation_3]

# one_square:
# 1
one_square_rotation_0 = [(0,0)]

one_square = [one_square_rotation_0]

# two_square:
# 1 1
# 1 1
two_square_rotation_0 = [(0,0), (0,1), (1,0), (1,1)]

two_square = [two_square_rotation_0]

# three_square:
# 1 1 1
# 1 1 1
# 1 1 1
three_square_rotation_0 = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]

three_square = [three_square_rotation_0]

# two_block:
# 1 1
two_block_rotation_0 = [(0,0), (1,0)]
two_block_rotation_1 = [(0,0), (0,1)]

two_block = [two_block_rotation_0, two_block_rotation_1]

# three_block:
# 1 1 1
three_block_rotation_0 = [(0,0), (1,0), (2,0)]
three_block_rotation_1 = [(0,0), (0,1), (0,2)]

three_block = [three_block_rotation_0, three_block_rotation_1]


# four_block:
# 1 1 1 1
four_block_rotation_0 = [(0,0), (1,0), (2,0), (3,0)]
four_block_rotation_1 = [(0,0), (0,1), (0,2), (0,3)]

four_block = [four_block_rotation_0, four_block_rotation_1]

# five_block:
# 1 1 1 1 1
five_block_rotation_0 = [(0,0), (1,0), (2,0), (3,0), (4,0)]
five_block_rotation_1 = [(0,0), (0,1), (0,2), (0,3), (0,4)]

five_block = [five_block_rotation_0, five_block_rotation_1]

# z_block_left:
#   1 1
# 1 1
z_block_left_rotation_0 = [(0,0), (1,0), (1,1), (2,1)]
# This one is complicated so we will write it
# 1 0
# 1 1
# 0 1
z_block_left_rotation_1 = [(1,0), (1,1), (0,1), (0,2)]

z_block_left = [z_block_left_rotation_0, z_block_left_rotation_1]

# z_block_right:
# 1 1
#   1 1
z_block_right_rotation_0 = [(0,1), (1,1), (1,0), (2,0)]
z_block_right_rotation_1 = [(0,0), (0,1), (1,1), (1,2)]

z_block_right = [z_block_right_rotation_0, z_block_right_rotation_1]

# corner_block_left:
# 1
# 1 1
corner_block_rotation_0 = [(0,0), (1,0), (0, 1)]
corner_block_rotation_1 = [(0,0), (0,1), (1,1)]
# This one is complicated so we will write it
# 1 1
# 0 1
corner_block_rotation_2 = [(0,1), (1,1), (1,0)]
corner_block_rotation_3 = [(0,0), (1,0), (1,1)]

corner_block = [corner_block_rotation_0, corner_block_rotation_1, corner_block_rotation_2, corner_block_rotation_3]


main_block_list = [L_left, L_right, one_square, two_square, three_square, 
                   two_block, three_block, four_block, five_block, z_block_right, 
                   z_block_left, corner_block]


def print_block(block):
    # Function to print a block into the console

    # 1. Find the dimensions of the block
    max_x = 0
    max_y = 0
    for cell in block:
        if cell[0] > max_y:
            max_y = cell[0]
        if cell[1] > max_x:
            max_x = cell[1]

    # 2. Create a grid to print the block
    grid = np.zeros((max_x+1, max_y+1), dtype=int)

    # 3. Fill in the grid with the block
    for cell in block:
        grid[cell[1], cell[0]] = 1

    # 4. Print the grid
    for row in grid:
        row_str = ""
        for cell in row:
            if cell == 1:
                row_str += "██"
            else:
                row_str += "  "
        print(row_str)
