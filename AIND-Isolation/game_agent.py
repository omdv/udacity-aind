"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(my_moves - 2*opp_moves)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    w, h = game.width / 2., game.height / 2.
    y_p, x_p = game.get_player_location(player)
    y_o, x_o = game.get_player_location(game.get_opponent(player))

    dist_center_p = float((h - y_p)**2 + (w - x_p)**2)
    dist_center_o = float((h - y_o)**2 + (w - x_o)**2)
    dist_players = float((y_p - y_o)**2 + (x_p - x_o)**2)

    return float(my_moves - 2*opp_moves + dist_players)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    w, h = game.width / 2., game.height / 2.
    y_p, x_p = game.get_player_location(player)
    y_o, x_o = game.get_player_location(game.get_opponent(player))

    dist_center_p = float((h - y_p)**2 + (w - x_p)**2)
    dist_center_o = float((h - y_o)**2 + (w - x_o)**2)
    dist_players = float((y_p - y_o)**2 + (x_p - x_o)**2)

    return float(my_moves - 2*opp_moves - dist_center_p)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    # book of opening moves
    def opening_book(self, game):
        moves = game.move_count
        if moves == 0:
            # provides ~5% by itself
            return (game.width // 2, game.height // 2)
        return False

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        # opening book
        opening = self.opening_book(game)
        if opening:
            return opening

        try:
            return self.minimax(game, self.search_depth)
        except SearchTimeout:
            pass

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        best_move = (-1, -1)
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        v = float("-inf")
        for m in game.get_legal_moves():
            new_v = self.min_value(game.forecast_move(m), 0, depth)
            if new_v > v:
                best_move = m
                v = new_v

        # graceful losing - no forfeiting
        if (v == float("-inf")) & (len(game.get_legal_moves()) > 0):
            moves = game.get_legal_moves()
            best_move = moves[random.randint(0, len(moves)-1)]

        return best_move

    # max value
    def max_value(self, game, depth, d_limit):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        depth += 1
        if depth == d_limit:
            return self.score(game, self)

        v = float("-inf")
        for m in game.get_legal_moves():
            v = max(v, self.min_value(game.forecast_move(m), depth, d_limit))
        return v

    # min value
    def min_value(self, game, depth, d_limit):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        depth += 1
        if depth == d_limit:
            return self.score(game, self)

        v = float("inf")
        for m in game.get_legal_moves():
            v = min(v, self.max_value(game.forecast_move(m), depth, d_limit))
        return v


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    # def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
    #     IsolationPlayer.__init__(self, search_depth, score_fn, timeout)
    #     self.depths = []
    #     self.legal_moves = []
    #     self.utility = {}

    # book of opening moves
    def opening_book(self, game):
        moves = game.move_count
        # central move first
        if moves == 0:
            return (game.width // 2, game.height // 2)
        return False

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        self.TIMER_THRESHOLD = 15
        depth_limit = 0

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        # # opening book moves
        # opening = self.opening_book(game)
        # if opening:
        #     self.depths.append(depth_limit)
        #     self.legal_moves.append(len(game.get_legal_moves()))
        #     return opening

        # main cycle
        try:
            while depth_limit < len(game.get_blank_spaces()):
                best_move = self.alphabeta(game, depth_limit)
                depth_limit += 1
            # best_moves.append[best_move]
        except SearchTimeout:
            pass

        # graceful forfeit
        legal_moves = game.get_legal_moves()
        if (best_move not in legal_moves) & (len(legal_moves) > 0):
            best_move = legal_moves[random.randint(0, len(legal_moves) - 1)]

        # # save for analysis purposes
        # self.depths.append(depth_limit)
        # self.legal_moves.append(len(game.get_legal_moves()))

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # initialization
        best_move = (-1, -1)

        # search
        _v, best_move = self.max_ab(game, float("-inf"), float("+inf"), 0, depth)

        return best_move

    # min value
    def min_ab(self, game, alpha, beta, depth, d_limit):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth >= d_limit:
            return self.score(game, self), (-1, -1)
        depth += 1

        v = float("inf")
        move = (-1, -1)

        for m in game.get_legal_moves():
            _g = game.forecast_move(m)
            _v, _ = self.max_ab(_g, alpha, beta, depth, d_limit)
            if _v < v:
                v = _v
                move = m

            if v <= alpha:
                return v, move
            beta = min(beta, v)
        return v, move

    # max value
    def max_ab(self, game, alpha, beta, depth, d_limit):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth >= d_limit:
            return self.score(game, self), (-1, -1)
        depth += 1

        v = float("-inf")
        move = (-1, -1)

        for m in game.get_legal_moves():
            _g = game.forecast_move(m)
            _v, _m = self.min_ab(_g, alpha, beta, depth, d_limit)
            if _v > v:
                v = _v
                move = m

            if v >= beta:
                return v, move
            alpha = max(alpha, v)
        return v, move


# used for testing
if __name__ == "__main__":
    from isolation import Board

    p1 = AlphaBetaPlayer(score_fn=custom_score_2)
    p2 = MinimaxPlayer(score_fn=custom_score_2)
    game = Board(p1, p2, width=7, height=7)
    winner, history, _ = game.play()

    # game.apply_move((1, 2))
    # game.apply_move((2, 2))
    # game.apply_move((2, 3))
    # game.apply_move((2, 4))
    # game.apply_move((3, 1))
    # game.apply_move((3, 3))
    # game.apply_move((3, 4))
    # game.apply_move((3, 6))
    # game.apply_move((4, 3))
    # game.apply_move((4, 4))
    # game.apply_move((4, 5))
    # game.apply_move((5, 2))
    # game.apply_move((5, 3))
    # game.apply_move((5, 4))
    # game.apply_move((5, 6))
    # game.apply_move((6, 2))
    # game.apply_move((6, 4))
    # game.apply_move((7, 4))
    # game.apply_move((6, 6))
    # game.apply_move((3, 5))

    # p1.alphabeta(game, 2)