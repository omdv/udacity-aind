from utils import *
from functools import reduce
from copy import deepcopy

def search(values, depth=0):
    """
    Using depth-first search and propagation, create a search tree and solve the sudoku.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if not values:
        return False

    # Choose one of the unfilled squares with the fewest possibilities
    unsolved_boxes = [box for box in values.keys() if len(values[box]) > 1]
    if len(unsolved_boxes) == 0:
        return values

    minbox = reduce(lambda x, y: y if len(values[y]) < len(values[x]) else x, unsolved_boxes, unsolved_boxes[0])

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for idx in range(len(values[minbox])):
        new_values = deepcopy(values)
        new_values[minbox] = new_values[minbox][idx]
        attempt = search(new_values, depth+1)
        if attempt:
            return attempt


# sudoku1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
# display(reduce_puzzle(grid_values(sudoku1)))

sudoku = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
# grid = grid_values(sudoku)
# display(reduce_puzzle(grid))
display(search(grid_values(sudoku)))