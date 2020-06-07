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


app = Flask(__name__)

GAME = Quarto()

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

    if GAME.selected:
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

@app.route("/")
def test_grid():
    game_state = json.dumps(parse_state())
    return render_template("pretty_quarto.html", game=game_state)

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
        print("played SELECT", piece)
    elif GAME.state == State.PLACE and int(cell) in GAME.options():
        cell_number = int(cell)
        GAME.transition(cell_number)
        print("played PLACE", cell_number)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
