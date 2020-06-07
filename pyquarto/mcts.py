"""
MCTS implementation for quarto
"""

import math

class MCTS:

    STATES = dict()

    def iterate(self, game):

        # setup
        if hash(game) not in self.STATES:
            self.add_state(game)

        # explore
        curr_game = game.copy()
        walked = []
        while not self.has_unexplored(curr_game):
            game_hash = hash(curr_game)
            walked.append(game_hash)
            self.STATES[game_hash]["n_pass"] += 1
            action = max(
                        self.STATES[game_hash]["succ"], 
                        key=lambda o : self.STATES[game_hash]["succ"][o][0],
                        )
            curr_game.transition(action)

            # update last move
        game_hash = hash(curr_game)
        walked.append(game_hash)
        self.STATES[game_hash]["n_pass"] += 1

        # expand
        expand_action = self.get_unexplored(curr_game)
        curr_game.transition(expand_action)
        new_hash = hash(curr_game)
        self.STATES[game_hash]["succ"][expand_action][1] = new_hash
        self.add_state(curr_game)
        self.STATES[new_hash]["n_pass"] += 1

        # rollout
        result = 1 if curr_game.random_rollout() == game.player else 0
        self.STATES[new_hash]["wins"] += result

        # update
        last_hash = new_hash
        for game_hash in reversed(walked):
            act = self._get_action_from_succ_hash(game_hash, last_hash)
            N = self.STATES[game_hash]["n_pass"]
            n = self.STATES[last_hash]["n_pass"]
            w = self.STATES[last_hash]["wins"]
            c = 1
            print(f"computing with w={w}, n={n}, N={N}")
            self.STATES[game_hash]["succ"][act][0] = w/n + c*math.sqrt(math.log(N)/n)
            self.STATES[game_hash]["wins"] += result
            last_hash = game_hash

    def decide(self, game):
        game_hash = hash(game)
        values = dict()
        for o in game.options():
            succ = self.STATES[game_hash]["succ"][o][1]
            w = self.STATES[succ]["wins"]
            n = self.STATES[succ]["n_pass"]
            values[o] = w/n

        return max(
                    values, 
                    key=lambda o : values[o],
                    )

            
    def _get_action_from_succ_hash(self, game_hash, succ_hash):

        for o, data in self.STATES[game_hash]["succ"].items():
            if data[1] == succ_hash:
                return o
        else:
            return None

    def add_state(self, game):
        self.STATES[hash(game)] = {
                "pred" : [],
                "succ" : {o:[math.inf, None] for o in game.options()},
                "n_pass" : 0,
                "wins" : 0,
            }



    def has_unexplored(self, game):
        return any(map(lambda o: o[0] == math.inf, self.STATES[hash(game)]["succ"].values()))

    def get_unexplored(self, game):
        return list(filter(lambda o: self.STATES[hash(game)]["succ"][o][0] == math.inf, self.STATES[hash(game)]["succ"]))[0]


if __name__ == "__main__":
    from quarto_logic import Quarto
    test = Quarto()
    mcts = MCTS()
    for _ in range(1000):
        mcts.iterate(test)

    print(mcts.STATES[hash(test)])
    print(mcts.decide(test))