import sys
import os

import json
from itertools import product

from flask import Flask, escape, request, render_template, url_for, redirect

# TODO : setup in venv with install pyquarto module
PYQUARTO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pyquarto")
print(PYQUARTO_PATH)
sys.path.append(PYQUARTO_PATH)

from quarto_logic import Quarto, State
from mcts import MCTS


app = Flask(__name__)

GAME = Quarto()
BOT = MCTS()
N_ITER = 1000

def get_pieces():
    result = list()
    for idx, piece in enumerate(Quarto.PIECES):
        result.append({
            "img" : "/static/images/" + "".join(map(str, piece)) + "S.png",
            "piece": idx,
            "im_id" : f"im{idx}",
        })
    return result

def get_board_array():
    """
    return a list of references to the pieces image names
    """
    result = list()
    for row, col in product(range(4), range(4)):

        piece = GAME.board[row*4+col]
        piece_id = ord(GAME.sym_board[row*4 + col]) - 65
        if (piece is None):
            result.append({
                "img" : None,
                "position" : [row, col],
                "piece": None,
                "im_id" : None,
            })
        else:
            result.append({
                "img" : "/static/images/" + "".join(map(str, piece)) +"S.png",
                "position" : [row, col],
                "piece": ord(GAME.sym_board[row*4 + col]) - 65,
                "im_id" : "im" + str(piece_id),
            })

    return result

def get_available_array():
    """
    return a list of references to the pieces image names
    """
    result = list()
    for idx, av in enumerate(GAME.available):
        if av == 0:
            result.append({
                "img" : None,
                "piece" : idx,
                "im_id" : f"im{idx}",
            })
        else:
            result.append({
                "img" : "/static/images/" + "".join(map(str, GAME.PIECES[idx])) + "S.png",
                "piece" : idx,
                "im_id" : f"im{idx}",
            })
    return result

def parse_state():

    board_pieces = get_board_array()
    available = get_available_array()

    if GAME.selected is not None:
        selected = {
            "img" : "/static/images/" + "".join(map(str, GAME.PIECES[GAME.selected])) + "S.png",
            "piece" : GAME.selected,
            "im_id" : f"""im{GAME.selected}"""
        }
    else:
        selected = None

    return {
        "all_pieces" : get_pieces(),
        "board_pieces" : board_pieces,
        "available" : available,
        "selected" : selected,
        "player" : GAME.player,
        "state" : str(GAME.state),
        }

from pprint import pprint

@app.route("/")
def run_game():
    print(GAME)
    parsed_state = parse_state()
    print(parsed_state["player"])
    print(parsed_state["state"])
    game_state = json.dumps(parse_state())
    
    return render_template("game.html", game=game_state)

@app.route("/new_game", methods=["POST"])
def reset():
    GAME.__init__()
    return redirect("/")


@app.route("/play", methods=["POST"])
def play():

    print("Played with request", request.form)
    cell = request.form.get("cell")
    if cell:
        row = int(cell) // 4
        col = int(cell) % 4
    piece = request.form.get("piece")

    if GAME.state == State.SELECT and int(piece) in GAME.options():

        GAME.transition(int(piece))

        # bot place
        for _ in range(N_ITER):
            BOT.iterate(GAME)
        bot_action = BOT.decide(GAME)
        print("Bot is placing:", bot_action)
        GAME.transition(bot_action)

        # bot select
        if GAME.end() == -1:
            for _ in range(N_ITER):
                BOT.iterate(GAME)
            bot_action = BOT.decide(GAME)
            print("Bot is selecting:", bot_action)
            GAME.transition(bot_action)
        
    elif GAME.state == State.PLACE and int(cell) in GAME.options():
        cell_number = int(cell)
        GAME.transition(cell_number)
        print("played PLACE", cell_number)

    if GAME.end() != -1:
        print(GAME)
        return render_template("end.html", game=json.dumps(parse_state()))
    else:
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
