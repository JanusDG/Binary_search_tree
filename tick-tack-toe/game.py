from board import Board, Branch
from os import system
import time
import pickle
import platform

def clean_screen():
    """
    cleans the user's console screen
    """
    if platform.system() == "Linux":
        system("clear")
    elif platform.system() == "Windows":
        system("cls")

def check_answer(board, answer):
    assert("," in answer or len(answer))
    assert(len(answer) == 3)
    assert(answer[0].isnumeric())
    assert(answer[-1].isnumeric())
    assert(int(answer[0]) in range(1,4))
    assert(int(answer[-1]) in range(1,4))
    assert(board.set_sign(True, [int(item) - 1 for item in answer.split(",")]))

def main():
    board = Board()
    # pickle is used to omit the process of building 
    # the tree of decisions that was done in board.py 

    with open("root.pickle","rb") as file:
        board.root = pickle.load(file)
    while not board.check_winner():
        clean_screen()
        print("you are playing for X")
        print()
        print(board)
        answer = input("Enter coordinates separated by coma ")
        while True:
            try:
                check_answer(board, answer)
                break
            except AssertionError:
                answer = input("Enter a free spot's coordinate in the right format to make a turn\n")

        if board.check_winner():
            clean_screen()
            print(board.check_winner())
            print()
            print(board)
            break
        board.make_a_move()
        if board.check_winner():
            clean_screen()
            print(board.check_winner())
            print()
            print(board)
            break

if __name__ == "__main__":
    main()