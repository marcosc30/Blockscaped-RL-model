from game import is_allowed, place_block
import numpy as np

def test_is_allowed():
    # Test case 1: Block can be placed at the given position
    grid = np.zeros((8, 8), dtype=int)
    block = [(0, 0), (0, 1), (1, 0), (1, 1)]
    x = 0
    y = 0
    assert is_allowed(grid, block, x, y) == True

    # Test case 2: Block exceeds grid boundaries
    grid = np.zeros((8, 8), dtype=int)
    block = [(0, 0), (0, 1), (1, 0), (1, 1)]
    x = 7
    y = 7
    assert is_allowed(grid, block, x, y) == False

    # Test case 3: Block overlaps with existing block
    grid = np.zeros((8, 8), dtype=int)
    grid[0, 0] = 1
    block = [(0, 0), (0, 1), (1, 0), (1, 1)]
    x = 0
    y = 0
    assert is_allowed(grid, block, x, y) == False

    # Test case 4: Block can be placed at the given position (empty grid)
    grid = np.zeros((8, 8), dtype=int)
    block = [(0, 0), (0, 1), (1, 0), (1, 1)]
    x = 3
    y = 3
    assert is_allowed(grid, block, x, y) == True

    # Test case 5: Block can be placed at the given position (non-empty grid)
    grid = np.zeros((8, 8), dtype=int)
    grid[2, 2] = 1
    block = [(0, 0), (0, 1), (1, 0), (1, 1)]
    x = 3
    y = 3
    assert is_allowed(grid, block, x, y) == True

test_is_allowed()

def test_place_block():
    # Test case 1: Block can be placed at the given position
    grid = np.zeros((8, 8), dtype=int)
    block = [(0, 0), (0, 1), (1, 0), (1, 1)]
    x = 0
    y = 0
    expected_grid = np.array([[1, 1, 0, 0, 0, 0, 0, 0],
                             [1, 1, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]])
    assert np.array_equal(place_block(grid, block, x, y), expected_grid)

    # Test case 2: Block can be placed at the given position (non-empty grid)
    grid = np.zeros((8, 8), dtype=int)
    grid[2, 2] = 1
    block = [(0, 0), (0, 1), (1, 0), (1, 1)]
    x = 3
    y = 3
    expected_grid = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 1, 0, 0, 0],
                             [0, 0, 0, 1, 1, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]])
    assert np.array_equal(place_block(grid, block, x, y), expected_grid)

    # Test case 3: Block exceeds grid boundaries
    grid = np.zeros((8, 8), dtype=int)
    block = [(0, 0), (0, 1), (1, 0), (1, 1)]
    x = 7
    y = 7
    expected_grid = np.zeros((8, 8), dtype=int)
    assert np.array_equal(place_block(grid, block, x, y), expected_grid)

test_place_block()