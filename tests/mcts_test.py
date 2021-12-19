"""
test mcts algorithm
"""

import statistics
import sys
import os
import pytest
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

import time
from logic.quarto_logic import Quarto
from logic.mcts import MCTS
from logic.mcts_quarto import QuartoInterface

def test_iterate():
    """
    test a basic iteration
    """
    game = Quarto()
    root = hash(game)
    mcts = MCTS(QuartoInterface)
    mcts.iterate(game)
    root_state = mcts.states[root]

    assert len(mcts.states) == 2
    assert root_state.N == 2

def test_time_iterations():

    game = Quarto()
    mcts = MCTS(QuartoInterface)

    start = time.time()
    for _ in range(1000):
        mcts.iterate(game)
    end = time.time()

    assert float(end - start) < 1

def test_winning_move():
    game = Quarto()
    mcts = MCTS(QuartoInterface)
    actions = [3, 0, 1, 5, 5, 10, 0]
    for a in actions:
        game.transition(a)
    for _ in range(2500):
        mcts.iterate(game)
    choice = mcts.chose(game)
    assert choice == 15

def test_losing_move():
    game = Quarto()
    mcts = MCTS(QuartoInterface)
    actions = [3, 0, 1, 5, 5, 10]
    for a in actions:
        game.transition(a)
    for _ in range(2500):
        mcts.iterate(game)
    choice = mcts.chose(game)
    assert choice != 0

@pytest.mark.parametrize('n_iter_players', ((50, 200), (200, 50)))
def test_mcts_compare(n_iter_players):
    n_sims = 20
    scores = [0, 0, 0]
    times = []
    for _ in range(n_sims):
        start = time.time()
        game = Quarto()
        players = [MCTS(QuartoInterface), MCTS(QuartoInterface)]
        while game.end() == -1:
            players[game.player].run(game, n_iter_players[game.player])
            action = players[game.player].chose(game)
            game.transition((action))
        end = time.time()
        scores[game.end()] += 1
        times.append((end- start))

    print(f"Evaluate MCTS(n_iter={n_iter_players[0]}) vs MCTS(n_iter={n_iter_players[1]}): {scores[0]/n_sims:.2%} vs {scores[1]/n_sims:.2%} ({scores[2]/n_sims:.2%} ties.)")
    print(f'Average game time: {statistics.mean(times)}')
    assert False

@pytest.mark.parametrize('n_iter_players', ((20, 200),))
def test_mcts_progressive(n_iter_players):
    """specific case : test that if we don't reset knowledge of a bot, it can enhance skill over different games"""
    n_sims = 100
    scores = [0, 0, 0]
    ten_first_scores = [0, 0, 0]
    ten_last_scores = [0, 0, 0]
    times = []
    player_0 = MCTS(QuartoInterface)
    for n_sim in range(n_sims):
        start = time.time()
        game = Quarto()
        player_1 = MCTS(QuartoInterface)
        players = [player_0, player_1]
        while game.end() == -1:
            players[game.player].run(game, n_iter_players[game.player])
            action = players[game.player].chose(game)
            game.transition((action))
        end = time.time()
        scores[game.end()] += 1

        if n_sim < n_sims*.1:
            ten_first_scores[game.end()] += 1
        elif n_sim >= n_sims*.9:
            ten_last_scores[game.end()] += 1

        times.append((end- start))

    decile = n_sims / 10
    print(f"Evaluate MCTS(memory) vs MCTS(no_memory): {scores[0]/n_sims:.2%} vs {scores[1]/n_sims:.2%} ({scores[2]/n_sims:.2%} ties.)")
    print(f"Ten first scores: {ten_first_scores[0]/decile:.2%} vs {ten_first_scores[1]/decile:.2%} ({ten_first_scores[2]/decile:.2%} ties.)")
    print(f"Ten last scores: {ten_last_scores[0]/decile:.2%} vs {ten_last_scores[1]/decile:.2%} ({ten_last_scores[2]/decile:.2%} ties.)")
    print(f'Average game time: {statistics.mean(times)}')

    assert False