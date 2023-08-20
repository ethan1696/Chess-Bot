import sys
sys.path.append('.')
from src.board_simulator.Board import Board
import random

import torch
import torch.nn as nn
import torch.nn.functional as F

"""
This chess engine uses a probability predictor to walk the game tree to determine an optimal move
"""


class Softermax(nn.Module):
    def __init__(self, dim=1):
        super(Softermax, self).__init__()
        self.dim = dim

    def forward(self, x):
        softplus_x = F.softplus(x)  # Applying softplus to each element in x
        return softplus_x / torch.sum(softplus_x, dim=self.dim, keepdim=True)

class Chess_CNN_m1(nn.Module):
    """
    This model predicts the first position of a move based on a board state. 
    Input features:
        6-channel 8x8 tensor, with each channel representing a piece on the board.
        Boards must be augmented so that the player's side is white. 
        Friendly (white) pieces are represented by 1, opposing pieces (black) pieces are represented by -1, and empty squares are represented by 0
    Output:
        An 8x8 tensor representing the probabilities of each square being the "starting" square
    """
    def __init__(self):
        super(Chess_CNN_m1, self).__init__()
        self.conv1 = nn.Conv2d(6, 32, kernel_size=3, stride=1, padding=1)
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv2d(32, 32, kernel_size=3, stride=1, padding=1)
        self.relu2 = nn.ReLU()
        self.fc1 = nn.Linear(64 * 32, 1024)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(1024, 64)
        self.smax = Softermax()

    def forward(self, x):
        x = x.float()
        x = self.conv1(x)
        x = self.relu1(x)
        x = torch.flatten(x, start_dim=1)
        x = self.fc1(x)
        x = self.relu3(x)
        x = self.fc2(x)
        x = self.smax(x)
        x = x.view(x.size(0), 8, 8)
        return x
    
class Chess_CNN_m2(nn.Module):
    """
    This model predicts the second position of a move based on a board state. 
    Input features:
        7-channel 8x8 tensor, with each of the first 6 channel representing a piece on the board.
        Boards must be augmented so that the player's side is white. 
        Friendly (white) pieces are represented by 1, opposing pieces (black) pieces are represented by -1, and empty squares are represented by 0
        Last channel is a one-hot 8x8 tensor representing the first position of the move
    Output:
        An 8x8 tensor representing the probabilities of each square being the "ending" square
    """
    def __init__(self):
        super(Chess_CNN_m2, self).__init__()
        self.conv1 = nn.Conv2d(7, 32, kernel_size=3, stride=1, padding=1)
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv2d(32, 32, kernel_size=3, stride=1, padding=1)
        self.relu2 = nn.ReLU()
        self.fc1 = nn.Linear(64 * 32, 1024)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(1024, 64)
        self.smax = Softermax()

    def forward(self, x):
        x = x.float()
        x = self.conv1(x)
        x = self.relu1(x)
        x = torch.flatten(x, start_dim=1)
        x = self.fc1(x)
        x = self.relu3(x)
        x = self.fc2(x)
        x = self.smax(x)
        x = x.view(x.size(0), 8, 8)
        return x

#Load all models

m1 = Chess_CNN_m1()
m1.load_state_dict(torch.load("src/engines/engine_v1/model_training/models/m1_v9.pth"), strict=False)

m2_PA = Chess_CNN_m2()
m2_KN = Chess_CNN_m2()
m2_BI = Chess_CNN_m2()
m2_RO = Chess_CNN_m2()
m2_QU = Chess_CNN_m2()
m2_KI = Chess_CNN_m2()

m2_PA.load_state_dict(torch.load("src/engines/engine_v1/model_training/models/m2_PA_v1.pth"), strict=False)
m2_KN.load_state_dict(torch.load("src/engines/engine_v1/model_training/models/m2_KN_v1.pth"), strict=False)
m2_BI.load_state_dict(torch.load("src/engines/engine_v1/model_training/models/m2_BI_v1.pth"), strict=False)
m2_RO.load_state_dict(torch.load("src/engines/engine_v1/model_training/models/m2_RO_v1.pth"), strict=False)
m2_QU.load_state_dict(torch.load("src/engines/engine_v1/model_training/models/m2_QU_v1.pth"), strict=False)
m2_KI.load_state_dict(torch.load("src/engines/engine_v1/model_training/models/m2_KI_v1.pth"), strict=False)

m2_dict = {
    "PA" : m2_PA,
    "KN" : m2_KN,
    "BI" : m2_BI,
    "RO" : m2_RO,
    "QU" : m2_QU,
    "KI" : m2_KI
}

#Hyperparameters
top_n = 3
CM_val = 20
SM_val = 0
def board2tensors_m1(board, side):
    pieces = ["PA", "KN", "BI", "RO", "QU", "KI"]

    fr, op = None, None
    
    if side == 'W':
        fr = 'W'
        op = 'B'
    else:
        fr = 'B'
        op = 'W'

    res = [[[0 for _ in range(8)] for _ in range(8)] for _ in range(6)]
    
    for p in range(len(pieces)):
        fr_map = board.board_state[f'{fr}_{pieces[p]}']
        op_map = board.board_state[f'{op}_{pieces[p]}']

        for i in range(8):
            for j in range(8):
                mask = 1 << (8 * i + j)
                if(side == 'B'):
                    i = 7 - i
                if fr_map & mask:
                    res[p][i][j] = 1
                if op_map & mask:
                    res[p][i][j] = -1

    return torch.tensor(res)

def coord2tensor(coord):
    res = [[0] * 8 for i in range(0, 8)]

    col = coord[1]
    row = coord[0]
    res[row][col] = 1
    return torch.tensor(res)

def transform_coord(coord, side):
    if side == 'B':
        return [coord[0], 7 - coord[1]]
    else:
        return coord[:]

def get_expected_gain(board, side, depth):
    if depth == 0:
        board.print_board()
        return 0
    op = None
    
    if side == 'W':
        op = 'B'
    else:
        op = 'W'
    
    board_side = board.WHITE if side == 'W' else board.BLACK

    move_list = board.get_all_moves(board_side)

    if len(move_list) == 0:
        if board.in_check(board_side):
            return -CM_val
        else:
            return -SM_val

    board_tensor = board2tensors_m1(board, side)
    with torch.no_grad():
        m1_probs = m1(board_tensor.unsqueeze(0)).squeeze(0)
    for move in move_list:
        coord1 = transform_coord(move[0][0], side)
        coord2 = transform_coord(move[0][1], side)
        piece1 = board.get_piece_at(move[0][0])[2:]
        m1_tensor = coord2tensor(coord1)
        m2_board = torch.cat((board_tensor, m1_tensor.unsqueeze(0)), dim=0)
        with torch.no_grad():
            m2_probs = m2_dict[piece1](m2_board.unsqueeze(0)).squeeze(0)
        
        move.append(m1_probs[coord1[0]][coord1[1]].item() * m2_probs[coord2[0]][coord2[1]].item())
    move_list = sorted(move_list, key = lambda x : -x[3])[:top_n]

    prob_sum = 0

    for move in move_list:
        prob_sum += move[3]
        move.append(-get_expected_gain(move[1], op, depth - 1))
    
    expected_gain = 0

    for move in move_list:
        expected_gain += (move[3] / prob_sum) * (move[2] + move[4])

    return expected_gain

print(get_expected_gain(Board(), 'W', 7))

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