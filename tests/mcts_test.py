"""
test mcts algorithm
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

import time
from logic.quarto_logic import Quarto
from logic.mcts import MCTS

def test_iterate():
    """
    test a basic iteration
    """
    game = Quarto()
    root = hash(game)
    mcts = MCTS()
    mcts.iterate(game)
    root_state = mcts.STATES[root]

    assert len(mcts.STATES) == 2
    assert root_state["n_pass"] == 1

def test_time_iterations():

    game = Quarto()
    mcts = MCTS()

    start = time.time()
    for _ in range(10000):
        mcts.iterate(game)
    end = time.time()

    assert float(end - start) < 1