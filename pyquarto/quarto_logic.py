
from copy import deepcopy
from enum import Enum

class State(Enum):
    SELECT = 0
    PLACE = 1
    END = 2

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
        return [i*[5, 3][diag_idx] for i in range(4)]

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

    def transition(self, action):
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
                    
                if action % 3 == 0:
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


        
if __name__ == '__main__':

    print("Testing quarto logic")

    test = Quarto()
    while test.state != State.END:
        print("Game :")
        print(test)
        print(hash(test))
        opt = {o : (o//4, o%4) if test.state == State.PLACE else "".join(map(str, test.PIECES[o])) for o in test.options()}
        print("Options :", opt)
        act = int(input("select action:"))
        print("Chosing :", act)
        test.transition(act)

        print("rows")
        print(test.row_common)
        print(test.row_empty)

        print("cols")
        print(test.col_common)
        print(test.col_empty)

        print("diags")
        print(test.diag_common)
        print(test.diag_empty)


    print(test)
    print(hash(test))
    print(test.end())
    print("---")

