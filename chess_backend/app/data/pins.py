import os
import json
from chess_backend.app.helpers.piece_pinner import get_pinned_pieces
from chess_backend.app.data.positions import load_positions_from_json

# Get the absolute path of the JSON file
json_filename = "pinned_pieces.json"
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), json_filename))

# This will store pinned pieces after each movement
def store_pinned_pieces(piece_positions: dict, white_bitboard, black_bitboard):
    white_pinned = get_pinned_pieces("white-king", piece_positions, white_bitboard, black_bitboard)
    black_pinned = get_pinned_pieces("black-king", piece_positions, white_bitboard, black_bitboard)

    all_pinned = {
        "white_pins": white_pinned,
        "black_pins": black_pinned
    }

    with open(file_path, 'w') as f:
        json.dump(all_pinned, f, indent=4)  # indent for pretty formatting


def load_pinned_pieces():
    with open(file_path, "r") as file:
        pins = json.load(file)
        white_pins, black_pins = pins["white_pins"], pins["black_pins"]
        return white_pins, black_pins

def reset_pinned_pieces():
    # Placeholder, this will store an empty dict
    piece_positions = load_positions_from_json()
    store_pinned_pieces(piece_positions, 0,0)