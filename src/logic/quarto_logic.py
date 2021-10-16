
from copy import deepcopy
from enum import Enum
from random import choice

class State(Enum):
    SELECT = 'Select'
    PLACE = 'Place'
    END = 'End'

class Quarto:

    PIECES = [
                [n // 8,
                (n % 8) // 4,
                (n % 4) // 2,
                n % 2]
                for n in range(16)
                ]

    def __init__(self):
        self.board = [None for _ in range(16)]
        self.sym_board = ["." for _ in range(16)]
        self.selected = None
        self.available = [1 for _ in range(16)]
        self.state = State.SELECT
        self.player = 0

        # meta data to avoid many loop to check for end of game
        self.row_common = [[None for _ in range(4)] for _ in range(4)]
        self.row_empty = [4 for _ in range(4)]
        self.col_common = [[None for _ in range(4)] for _ in range(4)]
        self.col_empty = [4 for _ in range(4)]
        self.diag_common = [[None for _ in range(4)] for _ in range(2)]
        self.diag_empty = [4 for _ in range(2)]

    @property
    def board_number(self):
        return [self.PIECES.index(p) if p else None for p in self.board]

    def copy(self):
        return deepcopy(self)

    def _cell_str(self, cell_idx):
        cell = self.board[cell_idx]
        if cell is None:
            return ("  ", "  ")
        else:
            return (f"{cell[0]}{cell[1]}", f"{cell[2]}{cell[3]}")

    def __str__(self):

        lines = list()
        for row in range(4):
            l1 = ""
            l2 = ""
            for cell in self._row(row):
                l1 += self._cell_str(cell)[0] + "|"
                l2 += self._cell_str(cell)[1] + "|"
            lines += [l1[:-1], l2[:-1], "--+--+--+--"]
        selected = "".join(map(str, self.PIECES[self.selected])) if self.selected else "None"
        return "\n".join(lines[:-1] + [selected])
            

    def __hash__(self):
        sym_selected = "." if self.selected is None else chr(65 + self.selected)
        return hash("".join(self.sym_board) + sym_selected)

    @staticmethod
    def _row(row_idx):
        return [row_idx*4 + i for i in range(4)]

    @staticmethod
    def _col(col_idx):
        return [i*4 + col_idx for i in range(4)]

    @staticmethod
    def _diag(diag_idx):
        """
        diag 0 : 0, 5, 10 ,15
        diag 1 : 3, 6,  9, 12
        """
        return [(i + diag_idx)*[5, 3][diag_idx] for i in range(4)]

    @staticmethod
    def _compare(piece_1, piece_2):
        return [piece_1[i] if piece_1[i] == piece_2[i] else None for i in range(4)]

    def options(self):
        if self.state == State.SELECT:
            return list(filter(lambda n: self.available[n], range(16)))
        else:
            return list(filter(lambda n: self.board[n] is None, range(16)))

    def end(self):
        """
        return 0 if player 0 wins, 1 if player 1 wins, 2 in case of a tie and -1 if game is not finished
        """

        if self.state == State.SELECT:
            return -1


        for row_idx in range(4):
            if self.row_empty[row_idx] == 0 and any(map(lambda c : c != None, self.row_common[row_idx])):
                return self.player

        for col_idx in range(4):
            if self.col_empty[col_idx] == 0 and any(map(lambda c : c != None, self.col_common[col_idx])):
                return self.player

        for diag_idx in range(2):
            if self.diag_empty[diag_idx] == 0 and any(map(lambda c : c != None, self.diag_common[diag_idx])):
                return self.player

        # care to check at end AFTER placement
        if sum(self.available) == 0:
            return 2

        return -1

    def transition(self, action: int):
        """
        transition do nothing if action is bad
        """
        if self.state == State.SELECT:
            if self.available[action]:
                self.available[action] = 0
                self.selected = action
                self.player = (self.player + 1) % 2
                self.state = State.PLACE
        
        elif self.state == State.PLACE:
            if self.board[action] is None:
                assert isinstance(self.selected, int)
                piece = self.PIECES[self.selected]
                sym_piece = chr(65 + self.selected)
                col = action % 4
                row = action // 4

                self.board[action] = piece
                self.sym_board[action] = sym_piece
                self.selected = None

                # make all updates needed
                
                if action % 5 == 0:
                    if self.diag_empty[0] == 4:
                        self.diag_common[0] = piece.copy()
                    else:
                        self.diag_common[0] = self._compare(piece, self.diag_common[0])
                    self.diag_empty[0] -= 1
                    
                if action != 0 and action % 3 == 0:
                    if self.diag_empty[1] == 4:
                        self.diag_common[1] = piece.copy()
                    else:
                        self.diag_common[1] = self._compare(piece, self.diag_common[1])
                    self.diag_empty[1] -= 1
                    

                if self.row_empty[row] == 4:
                    self.row_common[row] = piece.copy()
                else:
                    self.row_common[row] = self._compare(piece, self.row_common[row])

                if self.col_empty[col] == 4:
                    self.col_common[col] = piece.copy()
                else:
                    self.col_common[col] = self._compare(piece, self.col_common[col])

                self.row_empty[row] -= 1
                self.col_empty[col] -= 1

                if self.end() != -1:
                    self.state = State.END
                else:
                    self.state = State.SELECT

    def random_rollout(self):
        while self.state != State.END:
            self.transition(choice(self.options()))
        return self.end()

    def enhanced_rollout(self):
        while self.state != State.END:
            options = self.options()
            # check if there is a winning move
            if self.state == State.PLACE:
                for o in options:
                    row = o // 4
                    col = o % 4
                    piece = self.PIECES[self.selected]
                    if self.row_empty[row] == 1 and any(map(lambda k : k is not None, self._compare(piece, self.row_common[row]))):
                        action = o
                        break
                    if self.col_empty[col] == 1 and any(map(lambda k : k is not None, self._compare(piece, self.col_common[col]))):
                        action = o
                        break
                    if o%5 == 0 and self.diag_empty[0] == 1 and any(map(lambda k : k is not None, self._compare(piece, self.diag_common[0]))):
                        action = o
                        break
                    if o!=0 and o!=15 and o%3 == 0 and self.diag_empty[0] == 1 and any(map(lambda k : k is not None, self._compare(piece, self.diag_common[0]))):
                        action = o
                        break
                else:
                    action = choice(options)
            else:
                # not chosing winning pieces
                menacing = list()
                for p in filter(lambda n: self.board[n] is None, range(16)):
                    row = p // 4
                    col = p % 4
                    if self.row_empty[row] == 1:
                        menacing.append(self.row_common[row].copy())
                    if self.row_empty[col] == 1:
                        menacing.append(self.col_common[col].copy())
                    if p%5 and self.diag_empty[0] == 1:
                        menacing.append(self.diag_common[0].copy())
                    if p!=0 and p!=15 and p%3 and self.diag_empty[1] == 1:
                        menacing.append(self.diag_common[1].copy())
                if menacing:
                    remove_options = list()
                    for o in options:
                        piece = self.PIECES[o]
                        if any(map(lambda m : any(map(
                                            lambda f : f is not None,
                                            self._compare(piece, m),
                                            )), 
                                menacing)
                                ):
                            remove_options.append(o)
                    # todo : look intop this .. weird stuff down there
                    if len(remove_options) < len(options):
                        options = sorted(set(options) - set(remove_options))

                action = choice(options)
                        
            self.transition(action)
        return self.end()


        
if __name__ == '__main__':

    import time
    import statistics
    
    N_SIM = 10000
    
    print("Testing quarto logic random_rollout")
    sim_time = list()
    score = {
        -1 : 0,
        0 : 0,
        1 : 0,
        2 : 0,
    }
    for _ in range(N_SIM):
        game = Quarto()
        start = time.time()
        game.random_rollout()
        score[game.end()] += 1
        sim_time.append(time.time()-start)

    mean = statistics.mean(sim_time)
    print(f"Average time on {N_SIM} simulations:{mean*1000:.8f}ms")
    print(f"Tie frequency:{score[2]/N_SIM:.2%}")
    print(f"Player 0 win frequency:{score[0]/N_SIM:.2%}")
    print(f"Player 1 win frequency:{score[1]/N_SIM:.2%}")

    print()
    print("Testing quarto logic enhanced_rollout")
    sim_time = list()
    score = {
        -1 : 0,
        0 : 0,
        1 : 0,
        2 : 0,
    }
    for _ in range(N_SIM):
        game = Quarto()
        start = time.time()
        game.enhanced_rollout()
        score[game.end()] += 1
        sim_time.append(time.time()-start)

    mean = statistics.mean(sim_time)
    print(f"Average time on {N_SIM} simulations:{mean*1000:.8f}ms")
    print(f"Tie frequency:{score[2]/N_SIM:.2%}")
    print(f"Player 0 win frequency:{score[0]/N_SIM:.2%}")
    print(f"Player 1 win frequency:{score[1]/N_SIM:.2%}")


    

