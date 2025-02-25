import os
import json

# Get the absolute path of the JSON file
json_filename = "boards.json"
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), json_filename))

# Initial boards
init_white_bitboard = 0b00000000_00000000_00000000_00000000_00000000_00000000_11111111_11111111
init_black_bitboard = 0b11111111_11111111_00000000_00000000_00000000_00000000_00000000_00000000

def store_boards(white_bitboard, black_bitboard):
    """Stores the boards to later usage"""
    boards = {
        "white_bitboard": white_bitboard,
        "black_bitboard": black_bitboard
    }

    with open(file_path, 'w') as f:
        json.dump(boards, f, indent=4)  # indent for pretty formatting

def reset_boards():
    """ Reset from here so we don't have to import the boards"""
    store_boards(init_white_bitboard, init_black_bitboard)

def load_boards():
    with open(file_path, "r") as file:
        boards = json.load(file)
        white_bitboard, black_bitboard = boards["white_bitboard"], boards["black_bitboard"]
        return white_bitboard, black_bitboard


def print_bitboard(bitboard):
    """Helper function to visualize the board"""
    for rank in range(7, -1, -1): 
        row = []
        for file in range(8):
            square = rank * 8 + file
            if bitboard & (1 << square):  
                row.append("1 ")  
            else:
                row.append(". ") 
        print("".join(row))  
    print() 

if __name__ == "__main__":
    store_boards(init_white_bitboard, init_black_bitboard)