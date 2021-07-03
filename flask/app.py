import sys
import os

import json
from itertools import product

from flask import Flask, escape, request, render_template, url_for, redirect
from flask_cors import CORS

# TODO : setup in venv with install pyquarto module
PYQUARTO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pyquarto")
print(PYQUARTO_PATH)
sys.path.append(PYQUARTO_PATH)

from quarto_logic import Quarto, State
from mcts import MCTS


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

BOT = MCTS()
N_ITER = 1000

# def get_pieces():
#     result = list()
#     for idx, piece in enumerate(Quarto.PIECES):
#         result.append({
#             "img" : "/static/images/" + "".join(map(str, piece)) + "S.png",
#             "piece": idx,
#             "im_id" : f"im{idx}",
#         })
#     return result

# def get_board_array():
#     """
#     return a list of references to the pieces image names
#     """
#     result = list()
#     for row, col in product(range(4), range(4)):

#         piece = GAME.board[row*4+col]
#         piece_id = ord(GAME.sym_board[row*4 + col]) - 65
#         if (piece is None):
#             result.append({
#                 "img" : None,
#                 "position" : [row, col],
#                 "piece": None,
#                 "im_id" : None,
#             })
#         else:
#             result.append({
#                 "img" : "/static/images/" + "".join(map(str, piece)) +"S.png",
#                 "position" : [row, col],
#                 "piece": ord(GAME.sym_board[row*4 + col]) - 65,
#                 "im_id" : "im" + str(piece_id),
#             })

#     return result

# def get_available_array():
#     """
#     return a list of references to the pieces image names
#     """
#     result = list()
#     for idx, av in enumerate(GAME.available):
#         if av == 0:
#             result.append({
#                 "img" : None,
#                 "piece" : idx,
#                 "im_id" : f"im{idx}",
#             })
#         else:
#             result.append({
#                 "img" : "/static/images/" + "".join(map(str, GAME.PIECES[idx])) + "S.png",
#                 "piece" : idx,
#                 "im_id" : f"im{idx}",
#             })
#     return result

# def parse_state():

#     board_pieces = get_board_array()
#     available = get_available_array()

#     if GAME.selected is not None:
#         selected = {
#             "img" : "/static/images/" + "".join(map(str, GAME.PIECES[GAME.selected])) + "S.png",
#             "piece" : GAME.selected,
#             "im_id" : f"""im{GAME.selected}"""
#         }
#     else:
#         selected = None

#     return {
#         "all_pieces" : get_pieces(),
#         "board_pieces" : board_pieces,
#         "available" : available,
#         "selected" : selected,
#         "player" : GAME.player,
#         "state" : str(GAME.state),
#         }

# from pprint import pprint

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/quarto/<game_id>")
def quarto_play(game_id):
    return render_template("game.html", json.dumps({"game_id" : game_id}))

@app.route("/quarto/<game_id>/end")
def quarto_end(game_id):
    return render_template("end.html", json.dumps({"game_id" : game_id}))

if __name__ == "__main__":
    app.run(debug=True)
