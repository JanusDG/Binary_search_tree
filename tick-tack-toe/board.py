# from array import array2D
import copy
import pickle
import random

class Branch:
    def __init__(self, board):
        self.score = 0
        self.board = board
        self.children = []
    
    @property
    def absolute_score(self):
        return self.score + sum([item.absolute_score for item in self.children])

class Board:
    def __init__(self, set_up = None):
        if set_up:
            self.positions = set_up
        else:
            self.positions =[[None for i in range(3)] 
                              for j in range(3)]
        self.last_position = None
        self.last_sign = None
        self.root = None

    def __str__(self):
        rez = ""
        for item in self.positions:
            line = ""
            for sign in item:
                if sign is None:
                    line += "|_|"
                    continue
                else:
                    if sign:
                        line += " X "
                    else:
                        line += " O " 
            rez += line + "\n"
        
        return rez
    
    def set_sign(self, value, coord):
        if self.positions[coord[0]][coord[1]] is None:
            self.positions[coord[0]][coord[1]] = value
            if self.root is not None:
                for item in self.root.children:
                    if item.board.positions == self.positions:
                        self.root = item
            return self
        else:
            return False

    def check_winner(self):
        def list_of_equal(lst):
            if lst[0] is None:
                return False
            for first in lst:
                for second in lst:
                    if first != second:
                        return False

            winner = "X" if lst[0] == True else "O"
            return f"{winner} won"
                
        for item in self.positions:
            rez = list_of_equal(item)
            if rez:
                return rez
        
        for i in range(3):
            rez = list_of_equal([item[i] for item in self.positions]) 
            if rez:
                return rez

        rez = list_of_equal([self.positions[i][i] for i in range(3)])
        if rez:
            return rez
        
        rez = list_of_equal([self.positions[i][2-i] for i in range(3)])
        if rez:
            return rez

        free_space = False
        for item in self.positions:
            for sign in item:
                if sign is None:
                    free_space = True
                    break

        if not free_space:
            return "tie"
        
        return False

    def tree_of_decisions(self):
        self.root = Branch(self)
        def make_tree(current, turn):
            if current.board.check_winner() == "X won":
                current.score = - 1
            elif current.board.check_winner() == "O won":
                current.score = 1
            elif current.board.check_winner() == "tie":
                current.score = 0
            else:
                directions = [(i,j) for i in range(3) for j in range(3)]
                for item in directions:
                    cur_board = copy.deepcopy(current.board.positions)
                    m = Board(cur_board)
                    if m.set_sign(turn,item):
                        current.children.append(Branch(m))

                for child in current.children:
                    make_tree(child, not turn)

        make_tree(self.root, True)

    def make_a_move(self):

        def key(value):
            return value.absolute_score
        if 1 not in [item.score for item in self.root.children]:
            lst = []
            for item in self.root.children:
                if -1 not in [child.score for child in item.children]:
                    lst.append(item)
            if lst:
                ranked = sorted(lst, key=key)
            else:
                ranked = sorted(self.root.children, key=key)

            best = ranked[-1]
            equal = [item for item in ranked if item.absolute_score == best.absolute_score]
            move = random.choice(equal)
        else:
            for item in self.root.children:
                if item.score == 1:
                    move = item
    
        self.root = move
        self.positions = move.board.positions


if __name__ == "__main__":
    d = Board()
    d.tree_of_decisions()
    with open("root.pickle", "wb") as f:
        pickle.dump(d.root, f)
