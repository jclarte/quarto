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

        player = curr_game.player
        # rollout
        if curr_game.end() == -1:
            # end = curr_game.random_rollout()
            end = curr_game.enhanced_rollout()
        else:
            end = curr_game.end()
            self.STATES[new_hash]["complete"] = True

        if end == 0:
            result = [1, 0]
        elif end == 1:
            result = [0, 1]
        else:
            result = [0, 0]


        self.STATES[new_hash]["wins"][0] += result[0]
        self.STATES[new_hash]["wins"][1] += result[1]

        # update
        last_hash = new_hash
        for game_hash in reversed(walked):
            act = self._get_action_from_succ_hash(game_hash, last_hash)
            if act is None:
                return
            player = self.STATES[game_hash]["player"]
            if self.STATES[last_hash]["complete"]:
                self.STATES[game_hash]["succ"][act][0] = 0
                # check if all complete
                if all(map(lambda v : v[0] == 0, self.STATES[game_hash]["succ"].values())):
                    self.STATES[game_hash]["complete"] = True
                    for p in range(2):
                        if max([self.STATES[s]["wins"][p] for s in self.STATES[game_hash]["succ"]]) > 0:
                            self.STATES[game_hash]["wins"][p] = self.STATES[game_hash]["n_pass"]
                        else:
                            self.STATES[game_hash]["wins"][p] = 0
            else:

                N = self.STATES[game_hash]["n_pass"]
                n = self.STATES[last_hash]["n_pass"]
                w = self.STATES[last_hash]["wins"][player]
                c = 1
                # print(f"computing with w={w}, n={n}, N={N}")
                self.STATES[game_hash]["succ"][act][0] = w/n + c*math.sqrt(math.log(N)/n)

            self.STATES[game_hash]["wins"][0] += result[0]
            self.STATES[game_hash]["wins"][1] += result[1]
            last_hash = game_hash

    def decide(self, game):
        game_hash = hash(game)
        values = dict()
        for o in game.options():
            succ = self.STATES[game_hash]["succ"][o][1]
            if succ is None:
                print(f" o:{o} NO SUCC")
                continue
            w = self.STATES[succ]["wins"][game.player]
            n = self.STATES[succ]["n_pass"]
            print(f" o:{o} wins:{w} n_pass:{n}")
            values[o] = w/n
        print("values:", values)

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
                "wins" : [0, 0],
                "complete" : False,
                "player" : game.player,
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
