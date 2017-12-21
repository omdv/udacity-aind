from copy import deepcopy


class GameState:

    def __init__(self, state=False):
        self.w = 3
        self.h = 2
        board = [[0 for x in range(self.h)] for y in range(self.w)]

        # init state if nothing is passed in
        # turn is 1 if bot turn and 0 otherwise
        if not state:
            # mark lowest corner
            board[self.w-1][self.h-1] = 1
            self.state = {
                'board': board,
                'positions': [None, None],
                'turn': 1
            }
        else:
            self.state = state

    def forecast_move(self, move):
        """ Return a new board object with the specified move
        applied to the current game state.

        Parameters
        ----------
        move: tuple
            The target position for the active player's next move
        """
        state = deepcopy(self.state)

        if move not in self.get_legal_moves():
            print("Illegal move {}".format(move))
            return self.__class__(state)

        state['board'][move[0]][move[1]] = 1
        state['positions'][state['turn']] = move
        state['turn'] = 1 - state['turn']

        return self.__class__(state)

    def get_legal_moves(self):
        """ Return a list of all legal moves available to the
        active player.  Each player should get a list of all
        empty spaces on the board on their first move, and
        otherwise they should get a list of all open spaces
        in a straight line along any row, column or diagonal
        from their current position. (Players CANNOT move
        through obstacles or blocked squares.) Moves should
        be a pair of integers in (column, row) order specifying
        the zero-indexed coordinates on the board.
        """
        state = self.state
        board = state['board']

        # return all board if first turn and position is None
        if not state['positions'][state['turn']]:
            return [(x, y) for x in range(self.w) for y in range(self.h) if not board[x][y]]

        x_pos = state['positions'][state['turn']][0]
        y_pos = state['positions'][state['turn']][1]

        rays = [(1, 0), (-1, 0), (0, 1), (0, -1),
                (-1, -1), (-1, 1), (1, -1), (1, 1)]
        moves = []

        for dx, dy in rays:
            x = x_pos
            y = y_pos
            while 0 <= x + dx < self.w and 0 <= y + dy < self.h:
                x = x + dx
                y = y + dy
                if board[x][y]:
                    break
                else:
                    moves.append((x, y))

        return moves

    def display_board(self):
        """ Displaying board and positions """
        state = self.state
        board = state['board']
        pos = state['positions']

        for y in range(self.h):
            line = []
            for x in range(self.w):
                if pos[0] == (x, y):
                    line.append("O")
                elif pos[1] == (x, y):
                    line.append("B")
                else:
                    line.append(str(board[x][y]))

            line = "|".join(line)
            line = line.replace("1", "x")
            line = line.replace("0", ".")
            print(line)


def terminal_test(gameState):
    """ Return True if the game is over for the active player
    and False otherwise.
    """
    return not bool(gameState.get_legal_moves())  # by Assumption 1


def min_value(gameState):
    """ Return the value for a win (+1) if the game is over,
    otherwise return the minimum value over all legal child
    nodes.
    """
    if terminal_test(gameState):
        return 1  # by Assumption 2
    v = float("inf")
    for m in gameState.get_legal_moves():
        v = min(v, max_value(gameState.forecast_move(m)))
    return v


def max_value(gameState):
    """ Return the value for a loss (-1) if the game is over,
    otherwise return the maximum value over all legal child
    nodes.
    """
    if terminal_test(gameState):
        return -1  # by assumption 2
    v = float("-inf")
    for m in gameState.get_legal_moves():
        v = max(v, min_value(gameState.forecast_move(m)))
    return v



if __name__ == '__main__':

    print("Creating empty game board...")
    g = GameState()

    print("Getting legal moves for player 1...")
    p1_empty_moves = g.get_legal_moves()
    print("Found {} legal moves.".format(len(p1_empty_moves or [])))

    print("Applying move (0, 0) for player 1...")
    g1 = g.forecast_move((0, 0))

    print("Getting legal moves for player 2...")
    p2_empty_moves = g1.get_legal_moves()
    if (0, 0) in set(p2_empty_moves):
        print("Failed\n  Uh oh! (0, 0) was not blocked properly when " +
              "player 1 moved there.")
    else:
        print("Everything looks good!")

    g2 = g1.forecast_move((1, 1))
    g3 = g2.forecast_move((2, 0))
    g4 = g3.forecast_move((0, 1))
    # g5 = g4.forecast_move((0, 1))
