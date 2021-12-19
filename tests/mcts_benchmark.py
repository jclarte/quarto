"""
benchmarking et plotting some results for quarto mcts
"""

import time
import statistics
import sys
import os
import pytest

import matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from logic.quarto_logic import Quarto
from logic.mcts import MCTS
from logic.mcts_quarto import QuartoInterface




def plot_time_per_n_iter():
    times = []
    for n_iter in range(1, 1001):
        game = Quarto()
        bot = MCTS(QuartoInterface)
        start = time.time()
        bot.run(game, n_iter)
        end = time.time()
        sim_time = (end - start)
        print(f"n_iter={n_iter}, time={sim_time}")
        times.append(sim_time)
    plt.plot(times)
    plt.show()

def plot_memory_vs_no_memory():
    scores = [0, 0, 0]
    win_ratio = []
    n_iter = [20, 100]
    game = Quarto()
    bot_0 = MCTS(QuartoInterface)
    for n_sim in range(1, 101):
        game = Quarto()
        bot_1 = MCTS(QuartoInterface)
        start = time.time()
        while game.end() == -1:
            action = [bot_0, bot_1][game.player].run(game, n_iter[game.player])
            # print(f"Player {game.player} plays {game.state} {action}")
            game.transition(action)
        scores[game.end()] += 1
        win_ratio.append(scores[0]/n_sim)
        print(f"n_iter={n_sim}, win_ratio={win_ratio[-1]}")
    plt.plot(win_ratio)
    plt.show()

def plot_memory_vs_no_memory_alter():
    scores = [0, 0, 0]
    win_ratio = []
    n_iter = [20, 100]
    game = Quarto()
    bot_0 = MCTS(QuartoInterface)
    for n_sim in range(1, 101):
        game = Quarto()
        bot_1 = MCTS(QuartoInterface)
        start = time.time()
        while game.end() == -1:
            action = [bot_1, bot_0][game.player].run(game, n_iter[game.player])
            # print(f"Player {game.player} plays {game.state} {action}")
            game.transition(action)
        scores[game.end()] += 1
        win_ratio.append(scores[1]/n_sim)
        print(f"n_iter={n_sim}, win_ratio={win_ratio[-1]}")
    plt.plot(win_ratio)
    plt.show()


def plot_win_ratio_convergence():
    scores = [0, 0, 0]
    win_ratio_0 = []
    win_ratio_1 = []
    tie_ratio = []
    n_iter = [1000, 1000]
    game = Quarto()
    for n_sim in range(1, 101):
        game = Quarto()
        bot_0 = MCTS(QuartoInterface)
        bot_1 = MCTS(QuartoInterface)
        start = time.time()
        while game.end() == -1:
            action = [bot_1, bot_0][game.player].run(game, n_iter[game.player])
            # print(f"Player {game.player} plays {game.state} {action}")
            game.transition(action)
        scores[game.end()] += 1
        win_ratio_0.append(scores[0]/n_sim)
        win_ratio_1.append(scores[1]/n_sim)
        tie_ratio.append(scores[2]/n_sim)
        print(f"n_iter={n_sim}, win_ratio_0={win_ratio_0[-1]:.1%}, win_ratio_1={win_ratio_1[-1]:.1%}, tie_ratio_0={tie_ratio[-1]:.1%}")
    plt.plot(win_ratio_0)
    plt.plot(win_ratio_1)
    plt.plot(tie_ratio)
    plt.show()

if __name__ == '__main__':
    # plot_time_per_n_iter()
    # plot_memory_vs_no_memory()
    # plot_memory_vs_no_memory_alter()
    plot_win_ratio_convergence()
else:
    raise ImportError("Can't import this script")