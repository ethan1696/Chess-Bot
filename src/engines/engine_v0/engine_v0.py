import sys
sys.path.append("../board_simulator")
sys.path.append("../engines")

from Board import Board
import random

"""
This chess engine only looks at all possible moves and randomly chooses one. 

Only meant to be for testing. 
"""


def get_move(board : Board, side):
    """
    Gets the next 'optimal' move based on board state

    Args:
        board (Board): board that the move is made on
        side (int): Board.WHITE or Board.BLACK
    Returns:
        move (int list list): the 'optimal' move
    """
    move_list = board.get_all_moves(side)

    print(f"ENGINE -- num moves available: {len(move_list)}")

    index = 0

    if(len(move_list) > 1):
        index = random.randint(0, len(move_list) - 1)

    return move_list[index][0]