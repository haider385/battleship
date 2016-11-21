import os


SHIP_INFO = [
    ("Aircraft Carrier", 5),
    ("Battleship", 4),
    ("Submarine", 3),
    ("Cruiser", 3),
    ("Patrol Boat", 2)
]

BOARD_SIZE = 10
X_AXIS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
Y_AXIS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

VERTICAL_SHIP = '|'
HORIZONTAL_SHIP = '-'
EMPTY = 'O'
MISS = '.'
HIT = '*'
SUNK = '#'

def print_board(board):
    print()
    print_board_heading()
    print()
    rows = ''
    row_num = 1
    for row in board:
        print(" " + str(row_num).rjust(2) + " " + (" ".join(row)))
        row_num += 1
        
def clear_screen():
    """Function has been modified to clear the screen on a windows
       operating system as well as linux"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_board_heading():
    print("    " + " ".join([chr(c) for c in range(ord('A'), ord('A') + BOARD_SIZE)]), end='')


def get_coordinate(coordinate, board):
    """returns the value stored in a coordinate
       on the board by using the coordinate"""
    x_index = X_AXIS.index(coordinate[0])
    y_index = Y_AXIS.index(coordinate[1:])
    
    return board[y_index][x_index]


def replace_coordinate(coordinate, board, replacement):
    """Replaces a coordinate on the board"""
    column = X_AXIS.index(coordinate[0])
    row = Y_AXIS.index(coordinate[1:])
    split_row = list(board[row])  
    split_row[column] = replacement  
    board[row] = ''.join(split_row)
    
    return board

def print_boards(boards, hide_index=None, copy=None):
    """Both players' boards are passed in as a list,
       both boards are printed side by side"""
    if not copy:
        rows = [[],[]]
        all_rows = [s.replace(VERTICAL_SHIP, EMPTY) for s in boards[hide_index]]
        all_rows = [s.replace(HORIZONTAL_SHIP, EMPTY) for s in all_rows]
        rows[hide_index].append(all_rows)

        for i in [0, 1]:
            if not i == hide_index:
                rows[i].append(boards[i])
                    
        board_1 = rows[0][0]
        board_2 = rows[1][0]

    elif copy:
        board_1 = boards[0]
        board_2 = boards[1]
        
    row_num = 1
    print()
    print_board_heading()
    print("     ", end='')
    print_board_heading()
    print()
    
    for row_1, row_2 in zip(board_1, board_2):
        print(" " + str(row_num).rjust(2) + " " + (" ".join(row_1)), end='')
        print("      " + str(row_num).rjust(2) + " " + (" ".join(row_2)))
        row_num += 1

    
