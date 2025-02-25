import os
import json

# Get the absolute path of the JSON file
json_filename = "piece_positions.json"
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), json_filename))
bitboards = {
        "black-pawn-3": 48,
        "black-pawn-4": 49,
        "black-pawn-5": 50,
        "black-pawn-6": 51,
        "black-pawn-7": 52,
        "black-pawn-8": 53,
        "black-pawn-9": 54,
        "black-pawn-0": 55,
        "black-rook-1": 56,
        "black-knight-1": 57,
        "black-bishop-1": 58,
        "black-queen-1": 59,
        "black-king": 60,
        "black-bishop-2": 61,
        "black-knight-2": 62,
        "black-rook-2": 63,
        "white-rook-1": 0,
        "white-knight-1": 1,
        "white-bishop-1": 2,
        "white-queen-1": 3,
        "white-king": 4,
        "white-bishop-2": 5,
        "white-knight-2": 6,
        "white-rook-2": 7,
        "white-pawn-3": 8,
        "white-pawn-4": 9,
        "white-pawn-5": 10,
        "white-pawn-6": 11,
        "white-pawn-7": 12,
        "white-pawn-8": 13,
        "white-pawn-9": 14,
        "white-pawn-0": 15
    }

def save_positions_to_json(piece_positions):
    """ Guarda los bitboards en un archivo JSON en la ruta especificada."""
    # Guardar el diccionario en un archivo JSON
    with open(file_path, "w") as json_file:
            json.dump(piece_positions, json_file, indent=4)

def reset_positions():
    """ Reset from here to avoid extra importantions"""
    save_positions_to_json(bitboards)

def load_positions_from_json():
    """Load precomputed chess moves from a JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)
