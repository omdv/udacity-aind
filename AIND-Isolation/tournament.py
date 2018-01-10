"""Estimate the strength rating of a student defined heuristic by competing
against fixed-depth minimax and alpha-beta search agents in a round-robin
tournament.

NOTE: All agents are constructed from the student CustomPlayer implementation,
so any errors present in that class will affect the outcome.

The student agent plays a number of "fair" matches against each test agent.
The matches are fair because the board is initialized randomly for both
players, and the players play each match twice -- once as the first player and
once as the second player.  Randomizing the openings and switching the player
order corrects for imbalances due to both starting position and initiative.
"""
import itertools
import random
import warnings
import numpy as np

from collections import namedtuple, defaultdict

from isolation import Board
from sample_players import (RandomPlayer, open_move_score,
                            improved_score, center_score)
from game_agent import (MinimaxPlayer, AlphaBetaPlayer, custom_score,
                        custom_score_2, custom_score_3, custom_score_4,
                        custom_score_5, custom_score_6)
from scipy.stats import ttest_ind

NUM_REPEATS = 20
NUM_MATCHES = 10  # number of matches against each opponent
TIME_LIMIT = 150  # number of milliseconds before timeout

DESCRIPTION = """
This script evaluates the performance of the custom_score evaluation
function against a baseline agent using alpha-beta search and iterative
deepening (ID) called `AB_Improved`. The three `AB_Custom` agents use
ID and alpha-beta search with the custom_score functions defined in
game_agent.py.
"""

Agent = namedtuple("Agent", ["player", "name"])


def play_round(cpu_agent, test_agents, win_counts, num_matches):
    """Compare the test agents to the cpu agent in "fair" matches.

    "Fair" matches use random starting locations and force the agents to
    play as both first and second player to control for advantages resulting
    from choosing better opening moves or having first initiative to move.
    """
    timeout_count = 0
    forfeit_count = 0
    for _ in range(num_matches):

        games = sum([[Board(cpu_agent.player, agent.player),
                      Board(agent.player, cpu_agent.player)]
                    for agent in test_agents], [])

        # initialize all games with a random move and response
        for _ in range(2):
            move = random.choice(games[0].get_legal_moves())
            for game in games:
                game.apply_move(move)

        # play all games and tally the results
        for game in games:
            winner, _, termination = game.play(time_limit=TIME_LIMIT)
            win_counts[winner] += 1

            if termination == "timeout":
                timeout_count += 1
            elif termination == "forfeit":
                forfeit_count += 1

    return timeout_count, forfeit_count


def update(total_wins, wins):
    for player in total_wins:
        total_wins[player] += wins[player]
    return total_wins


def play_matches(cpu_agents, test_agents, num_matches):
    """Play matches between the test agent and each cpu_agent individually. """
    total_wins = {agent.player: 0 for agent in test_agents}
    total_timeouts = 0.
    total_forfeits = 0.
    total_matches = 2 * num_matches * len(cpu_agents)

    print("\n{:^9}{:^13}".format("Match #", "Opponent") + ''.join(['{:^13}'.format(x[1].name) for x in enumerate(test_agents)]))
    print("{:^9}{:^13} ".format("", "") +  ' '.join(['{:^5}| {:^5}'.format("Won", "Lost") for x in enumerate(test_agents)]))

    for idx, agent in enumerate(cpu_agents):
        wins = {key: 0 for (key, value) in test_agents}
        wins[agent.player] = 0

        print("{!s:^9}{:^13}".format(idx + 1, agent.name), end="", flush=True)

        counts = play_round(agent, test_agents, wins, num_matches)
        total_timeouts += counts[0]
        total_forfeits += counts[1]
        total_wins = update(total_wins, wins)
        _total = 2 * num_matches
        round_totals = sum([[wins[agent.player], _total - wins[agent.player]]
                            for agent in test_agents], [])
        print(' ' + ' '.join([
            '{:^5}| {:^5}'.format(
                round_totals[i],round_totals[i+1]
            ) for i in range(0, len(round_totals), 2)
        ]))

    print("-" * 74)
    print('{:^9}{:^13}'.format("", "Win Rate:") +
        ''.join([
            '{:^13}'.format(
                "{:.1f}%".format(100 * total_wins[x[1].player] / total_matches)
            ) for x in enumerate(test_agents)
    ]))

    if total_timeouts:
        print(("\nThere were {} timeouts during the tournament -- make sure " +
               "your agent handles search timeout correctly, and consider " +
               "increasing the timeout margin for your agent.\n").format(
            total_timeouts))
    if total_forfeits:
        print(("\nYour agents forfeited {} games while there were still " +
               "legal moves available to play.\n").format(total_forfeits))

    return total_wins


def main():

    # Define two agents to compare -- these agents will play from the same
    # starting position against the same adversaries in the tournament
    test_agents = [
        # Agent(MinimaxPlayer(score_fn=custom_score), "MM_Custom"),
        # Agent(MinimaxPlayer(score_fn=custom_score_2), "MM_Custom_2"),
        # Agent(MinimaxPlayer(score_fn=custom_score_3), "MM_Custom_3"),
        Agent(AlphaBetaPlayer(score_fn=custom_score), "AB_Custom"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_2), "AB_Custom_2"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_3), "AB_Custom_3"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_4), "AB_Custom_4"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_5), "AB_Custom_5"),
        # Agent(AlphaBetaPlayer(score_fn=custom_score_6), "AB_Custom_6"),
        # Agent(AlphaBetaPlayer(score_fn=open_move_score), "AB_Open"),
        # Agent(AlphaBetaPlayer(score_fn=center_score), "AB_Center"),
        Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved"),
        # Agent(RandomPlayer(), "Random")
    ]

    # Define a collection of agents to compete against the test agents
    cpu_agents = [
        # Agent(RandomPlayer(), "Random"),
        # Agent(MinimaxPlayer(score_fn=open_move_score), "MM_Open"),
        # Agent(MinimaxPlayer(score_fn=center_score), "MM_Center"),
        # Agent(MinimaxPlayer(score_fn=improved_score), "MM_Improved"),
        # Agent(AlphaBetaPlayer(score_fn=open_move_score), "AB_Open"),
        # Agent(AlphaBetaPlayer(score_fn=center_score), "AB_Center"),
        Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved")
    ]

    print(DESCRIPTION)
    print("{:^74}".format("*************************"))
    print("{:^74}".format("Playing Matches"))
    print("{:^74}".format("*************************"))

    test_scores = defaultdict(list)
    for i in range(NUM_REPEATS):
        print(" " * 74)
        print("{:>37}{:d}".format("Sample ", i+1))
        print("-" * 74)
        wins = play_matches(cpu_agents, test_agents, NUM_MATCHES)
        for a in test_agents:
            test_scores[a.name].append(wins[a.player]/NUM_MATCHES)
    return wins, test_scores


def compare_populations(scores):
    print("^" * 74)
    print("{:^74}".format("*************************"))
    print("{:^74}".format("Statistical testing"))
    print("{:^74}".format("*************************"))
    benchmark = scores['AB_Improved']
    print('{:>30} | {:>10} | {:>10} | {:>10} | {:>10}'.
          format('Agent', 'mean', 'std', 'p-value', 'different?'))
    for a in list(scores):
        means = np.mean(scores[a])
        std = np.std(scores[a])
        pvalue = ttest_ind(scores[a], benchmark, equal_var=False).pvalue
        sign = str(pvalue < 0.05)
        print('{:>30} | {:10.3f} | {:10.3f} | {:10.4f} | {:>10}'.
              format(a, means, std, pvalue, sign))


if __name__ == "__main__":
    wins, ts = main()
    if NUM_REPEATS > 1:
        compare_populations(ts)
