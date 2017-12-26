from isolation import Board
from sample_players import (RandomPlayer, open_move_score,
                            improved_score, center_score)
from game_agent import (MinimaxPlayer, AlphaBetaPlayer, custom_score,
                        custom_score_2, custom_score_3)


def testing():
    p1 = MinimaxPlayer(score_fn=custom_score_2)
    p2 = AlphaBetaPlayer(score_fn=custom_score_2)
    

    game = Board(p1, p2, width=5, height=5)
    game.apply_move((3, 3))
    game.apply_move((0, 1))
    game.apply_move((0, 1))

    result = game.play()
    return result


if __name__ == "__main__":
    player, history, end = testing()
