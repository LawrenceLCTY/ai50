"""
Tic Tac Toe Player
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    move_count = 0
    while move_count <= 9:
        for row in board:
            for cell in row:
                if cell != EMPTY:
                    move_count += 1 
                else:
                    pass
        if move_count % 2 == 0:
            return O
        else:
            return X

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    available = set()

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                available.add((i,j))
    if len(available) == 0:
        return None
    else:
        return available    

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result_board = copy.deepcopy(board)
    if action in actions(board):
        result_board[action[0]][action[1]] = player(result_board)
    else:
        print('not available move')

    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if (
        (X == board[0][0] == board[0][1] == board[0][2])        #horizontal top
        or (X == board[1][0] == board[1][1] == board[1][2])     #horizontal middle
        or (X == board[2][0] == board[2][1] == board[2][2])     #horizontal bottom
        or (X == board[0][0] == board[1][0] == board[2][0])     #vertical left
        or (X == board[0][1] == board[1][1] == board[2][1])     #vertical middle
        or (X == board[0][2] == board[1][2] == board[2][2])     #vertical right
        or (X == board[0][0] == board[1][1] == board[2][2])     #diagonal \
        or (X == board[0][2] == board[1][1] == board[2][0])     #diagonal /
    ):
        return X
    elif (
        (O == board[0][0] == board[0][1] == board[0][2])        #horizontal top
        or (O == board[1][0] == board[1][1] == board[1][2])     #horizontal middle
        or (O == board[2][0] == board[2][1] == board[2][2])     #horizontal bottom
        or (O == board[0][0] == board[1][0] == board[2][0])     #vertical left
        or (O == board[0][1] == board[1][1] == board[2][1])     #vertical middle
        or (O == board[0][2] == board[1][2] == board[2][2])     #vertical right
        or (O == board[0][0] == board[1][1] == board[2][2])     #diagonal \
        or (O == board[0][2] == board[1][1] == board[2][0])     #diagonal /
    ):
        return O
    else:
        return None
       

    raise NotImplementedError

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None or actions(board) == None:
        return True
    else:
        return False

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
   
    raise NotImplementedError

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:                     #game over
        return None

    elif board == initial_state():                  #randomly choose first move
        i = random.randint(0,2)
        j = random.randint(0,2)
        return (i,j)

    elif player(board) == X:                        #AI plays as X
        util = -math.inf
        for action in actions(board):
            value = min_val(result(board, action))
            if value > util:
                util = value
                best_move = action
    else:                                           #AI plays as O
        util = math.inf
        for action in actions(board):
            value = max_val(result(board, action))
            if value < util:
                util = value
                best_move = action
    return best_move


def max_val(board):
    if terminal(board) == True:
        return utility(board)    
    value = -math.inf
    for action in actions(board):
        value = max(value,min_val(result(board,action)))
    return value


def min_val(board):
    if terminal(board) == True:
        return utility(board)
    value = math.inf
    for action in actions(board):
        value = min(value,max_val(result(board,action)))
    return value