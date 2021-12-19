"""
implementation of MCTS algorithm
"""
from abc import ABC, abstractmethod
import logging
from math import sqrt, log
from typing import Any, List, NewType, Optional

# logging.basicConfig(level='DEBUG')
LOG = logging.getLogger(__name__)

GameState = NewType('GameState', Any)

class GameInterface(ABC):
    """
    base class used by mcts for games
    any game using MCTS should implements this interface
    """
    @classmethod
    @abstractmethod
    def n_players(cls) -> int:
        """return the number of players of the game"""

    @classmethod
    @abstractmethod
    def transition(cls, state: GameState, option: Any) -> GameState:
        """return state of the game after doing option from state"""

    @classmethod
    @abstractmethod
    def options(cls, state: GameState) -> List[Any]:
        """return the list of available opions from state"""

    @classmethod
    @abstractmethod
    def end(cls, state: GameState) -> bool:
        """return True if game has ended"""

    @classmethod
    @abstractmethod
    def score(cls, state: GameState) -> List[int]:
        """return a list of score for every player"""

    @classmethod
    @abstractmethod
    def player(cls, state: GameState) -> int:
        """return the player number as int"""

    @classmethod
    @abstractmethod
    def hash(cls, state: GameState) -> int:
        """return a hash value for a game state"""

    @classmethod
    @abstractmethod
    def rollout(cls, state: GameState) -> Any:
        """rollout method is expected to generate an ended game state from state by any method"""


# exploration parameter for ucb
C = 1.41


class MCTS:
    """
    data structure for stored state is
    key=hash value of state
        state=game_state
        children=dict[option:hash(game_state) or None]
        score=[player0 score, player1 score]
        passed=number of times on this state
    """

    class _Node:
        game: Optional[GameInterface] = None

        def __init__(self, state: GameState) -> None:
            """class for stored games"""
            assert self.game, "_Node.game not initialised. You should use _Node.set_game(GameInterface)"
            self.state = state.copy()
            self.N = 1
            self.score = self.game.score(state)
            self.children = {o: None for o in self.game.options(state)}

        def __repr__(self) -> str:
            return f"Node(state={self.state}, N={self.N}, score={self.score}, children={self.children})"

        @classmethod
        def set_game(cls, game: GameInterface) -> None:
            cls.game = game
            LOG.debug(f"Set _Node.game = {game}")

    def __init__(self, game: GameInterface) -> None:
        self.states = dict()
        self.walked = set()
        self.game = game
        self._Node.set_game(game)

    @staticmethod
    def compute_ucb(w: int, n: int, N: int) -> float:
        """compute a ucb value"""
        return w/n + C*sqrt(log(N)/n)

    def explore(self, state: GameState) -> Any:

        LOG.debug(f"Exploring from state {state}")

        if self.game.end(state):
            LOG.debug(f"Game state is at end")
            return state

        ucb = dict()
        state_hash = self.game.hash(state)
        self.walked.add(state_hash)
        node = self.states[state_hash]
        for option, game_hash in node.children.items():
            if game_hash is None:
                LOG.debug(f"Unexplored node found for action {option}")
                resulting_state = self.game.transition(state, option)
                new_hash = self.game.hash(resulting_state)
                node.children[option] = new_hash
                return resulting_state
            game_node = self.states[game_hash]
            player = self.game.player(state)
            w = game_node.score[player]
            n = game_node.N
            N = node.N
            ucb[option] = self.compute_ucb(w, n, N)
        chosen_option = max(ucb, key=lambda k: ucb[k])
        resulting_state = self.game.transition(state, chosen_option)
        node.children[chosen_option] = self.game.hash(resulting_state)
        
        return self.explore(resulting_state)

    def expand(self, state: GameState) -> Any:
        LOG.debug(f"Expanding state {state}")
        # if self.game.end(state):
        #     LOG.debug(f"Game state is at end")
        #     return state

        game_hash = self.game.hash(state)
        self.states[game_hash] = self._Node(state)
        self.walked.add(game_hash)
        return state

    def rollout(self, state: GameState) -> Any:
        LOG.debug(f"Rollout from state {state}")
        if self.game.end(state):
            LOG.debug(f"Game state is at end")
            return state
        return self.game.rollout(state)

    def update(self, state: GameState) -> None:

        assert self.game.end(state)
        score = self.game.score(state)
        for walked_state in self.walked:
            for idx, value in enumerate(score):
                self.states[walked_state].score[idx] += value
            self.states[walked_state].N += 1
        self.walked = set()

    def iterate(self, state: GameState) -> None:
        """an iteration of MCTS"""
        LOG.debug(f"New iteration from state {state}")
        # LOG.debug(f" * States: {self.states}")
        LOG.debug(f" * Nb States: {len(self.states)}")
        
        if self.game.hash(state) not in self.states:
            self.expand(state)
        explored_state = self.explore(state)
        expanded_state = self.expand(explored_state)
        rollout_state = self.rollout(expanded_state)
        LOG.debug(f" * Walked: {self.walked}")
        self.update(rollout_state)

    def chose(self, state: GameState) -> Any:
        """return the chosen option"""
        scores = dict()
        player = self.game.player(state)
        game_hash = self.game.hash(state)
        assert game_hash in self.states, "Can't chose action for unknown state."
        node = self.states[game_hash]
        for option, game_node_hash in node.children.items():

            if game_node_hash is None:
                LOG.debug(f"Unexplored option {option}")
                continue
            game_node = self.states[game_node_hash]
            w = game_node.score[player]
            n = game_node.N
            win_ratio = w/n
            scores[option] = win_ratio
        LOG.debug(f"Actions : {scores}")
        return max(scores, key=lambda k: scores[k])

    def run(self, state: GameState, n_iterations: int = 100) -> Any:
        """make n iterations and return the chosen option"""
        for _ in range(n_iterations):
            self.iterate(state)
        LOG.debug(f"States: {self.states}")
        return self.chose(state)

