from copy import deepcopy
from functools import reduce


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
            return [(x, y) for x in range(self.w) for y in range(self.h) if board[x][y] != 1]

        x_pos = state['positions'][state['turn']][0]
        y_pos = state['positions'][state['turn']][1]

        # calculate legal vertical
        legal_v = []
        for y in range(y_pos-1, -1, -1):
            if board[x_pos][y] == 1:
                break
            else:
                legal_v.append((x_pos, y))

        for y in range(y_pos+1, self.h, +1):
            if board[x_pos][y] == 1:
                break
            else:
                legal_v.append((x_pos, y))

        # calculate legal horizontal
        legal_h = []
        for x in range(x_pos-1, -1, -1):
            if board[x][y_pos] == 1:
                break
            else:
                legal_h.append((x, y_pos))

        for x in range(x_pos+1, self.w, +1):
            if board[x][y_pos] == 1:
                break
            else:
                legal_h.append((x, y_pos))

        # calculate legal diagonal
        legal_d = []
        # Northwest
        for delta in range(1, max([x_pos+1, y_pos+1])):
            x = x_pos - delta
            y = y_pos - delta
            try:
                if board[x][y] == 1:
                    break
                if board[x][y] == 0:
                    legal_d.append((x, y))
            except:
                pass

        # Southeast
        for delta in range(1, max([self.w-x_pos+1, self.h-y_pos+1])):
            x = x_pos + delta
            y = y_pos + delta
            try:
                if board[x][y] == 1:
                    break
                if board[x][y] == 0:
                    legal_d.append((x, y))
            except:
                pass

        # Northeast
        for delta in range(1, max([x_pos+1, self.h-y_pos+1])):
            x = x_pos - delta
            y = y_pos + delta
            try:
                if board[x][y] == 1:
                    break
                if board[x][y] == 0:
                    legal_d.append((x, y))
            except:
                pass

        # Southwest
        for delta in range(1, max([self.w-x_pos+1, y_pos+1])):
            x = x_pos - delta
            y = y_pos + delta
            try:
                if board[x][y] == 1:
                    break
                if board[x][y] == 0:
                    legal_d.append((x, y))
            except:
                pass

        return legal_v+legal_h+legal_d

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
            line = line.replace("1","x")
            line = line.replace("0",".")
            print(line)


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