import sys
import os
import uuid

from flask import Flask
from flask_restful import Api, Resource

# TODO : setup in venv with install pyquarto module
PYQUARTO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pyquarto")
print(PYQUARTO_PATH)
sys.path.append(PYQUARTO_PATH)

from quarto_logic import Quarto, State

# TODO -> clean useless games
GAME_STACK = {}

app = Flask("pyquarto")
api = Api(app)

class GameBuilder(Resource):
    def get(self):
        game_id = str(uuid.uuid4()).replace("-", "")
        GAME_STACK[game_id] = Quarto()
        return {
            'id' : game_id, 
            'game' : GAME_STACK[game_id].to_dict(),
            }

class Play(Resource):
    def put(self, game_id, action):
        game = GAME_STACK.get(game_id)
        if not game:
            return {}

        game.transition(action)
        return {
            'id' : game_id,
            'game' : game.to_dict(),
            }

class Status(Resource):
    def get(self, game_id):
        game = GAME_STACK.get(game_id)
        if not game:
            return {}

        return {
            'id' : game_id,
            'state' : str(game.state),
            }

class End(Resource):
    def put(self, game_id):
        if game_id in GAME_STACK:
            del GAME_STACK[game_id]

        return {}

class Simulate(Resource):

    def get(self, game_id):
        game = GAME_STACK.get(game_id)
        if not game:
            return {}

        result = game.copy().enhanced_rollout()

        return {
            'id' : game_id,
            'result' : result,
            }



api.add_resource(GameBuilder, '/new_game')
api.add_resource(Play, '/<string:game_id>/play/<int:action>')
api.add_resource(Status, '/<string:game_id>/status')
api.add_resource(End, '/<string:game_id>/end')
api.add_resource(Simulate, '/<string:game_id>/simulate')

if __name__ == '__main__':
    app.run(debug=True)