
from utils import *
from functools import reduce


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
diag_1 = [list(map("".join, list(zip(rows, cols))))]
diag_2 = [list(map("".join, list(zip(rows, '987654321'))))]
unitlist = unitlist + diag_1 + diag_2

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def twin_counter(values):
    """Find twins in the provided list of values"""
    twins = []
    if len(set(values)) == len(values):
        return False
    else:
        for value in values:
            if values.count(value) == 2:
                twins.append(value)
    return list(set(twins))


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # process only once
    new_values = values.copy() 

    # get candidates for consideration
    two_digit_boxes = [box for box in values if len(values[box]) == 2]
    unit_twins = [[twin for twin in two_digit_boxes if twin in unit] for unit in unitlist]

    for idx, unit in enumerate(unitlist):
        if len(unit_twins[idx]) >= 2:
            twin_values = [values[twin] for twin in unit_twins[idx]]
            twins = twin_counter(twin_values)
            if twins:
                # loop in case there are >2 pairs
                for twin in twins:
                    # remove twin values from peers
                    for peer in unit:
                        if (len(values[peer]) > 1) and (twin != values[peer]):
                            new_values[peer] = new_values[peer].replace(twin[0], '')
                            new_values[peer] = new_values[peer].replace(twin[1], '')

    return new_values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False

    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
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
        new_values = values.copy()
        new_values[minbox] = new_values[minbox][idx]
        attempt = search(new_values)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    # try:
    #     import PySudoku
    #     PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    # except SystemExit:
    #     pass
    # except:
    #     print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
