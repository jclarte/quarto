from typing import List
from .mcts import GameInterface, GameState
from .quarto_logic import Quarto, State

class QuartoState(Quarto):
    """class inheriting both class"""

class QuartoInterface(GameInterface):

    @staticmethod
    def transition(state: QuartoState, action: int) -> GameState:
        action = int(action)
        new_game = state.copy()
        new_game.transition(action)
        return new_game

    @staticmethod
    def options(state: QuartoState):
        return state.options()

    @staticmethod
    def n_players() -> int:
        return 2
    
    @staticmethod
    def end(state: QuartoState) -> bool:
        """return True if game has ended"""
        return state.end() != -1
    
    @staticmethod
    def score(state: GameState) -> List[int]:
        """
        return a list of score for every player
        reminder for end result :
        -1: not finished
        0: player 0 wins
        1: player 1 wins
        2: tie
        """
        game_result = state.end()
        return [
            [1, 0],
            [0, 1],
            [0, 0]
        ][game_result]
    
    @staticmethod
    def player(state: QuartoState) -> int:
        """return the player number as int"""
        return state.player
    
    @staticmethod
    def hash(state: QuartoState) -> int:
        """return a hash value for a game state"""
        return hash(state)
    
    @staticmethod
    def rollout(state: QuartoState) -> QuartoState:
        """rollout method is expected to generate an ended game state from state by any method"""
        new_state = state.copy()
        new_state.enhanced_rollout()
        return new_state