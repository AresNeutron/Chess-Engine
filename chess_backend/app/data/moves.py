import json
import os
from chess_backend.app.non_sliding_pieces.king_and_knight import knight_lookup, king_lookup
from chess_backend.app.non_sliding_pieces.pawn import generate_pawn_moves
from chess_backend.app.sliding_pieces.moves import generate_sliding_moves

# Get the absolute path of the JSON file
json_filename = "chess_moves.json"
folder_name = "computed_moves"
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), folder_name, json_filename))

def save_moves_to_json(data):
    """Guarda los movimientos de ajedrez precomputados en un archivo JSON."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def load_moves_from_json():
    """Load precomputed chess moves from a JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)

if __name__ == "__main__":
    # Generar movimientos de peones
    white_pawn_moves, black_pawn_moves, white_pawn_attacks, black_pawn_attacks = generate_pawn_moves()

    # Generar movimientos de piezas deslizantes
    bishop_masks, bishop_moves, rook_masks, rook_moves = generate_sliding_moves()

    # Estructurar los movimientos precomputados
    precomputed_moves = {
        "pawn": {
            "white": {
                "moves": white_pawn_moves,
                "attacks": white_pawn_attacks
            },
            "black": {
                "moves": black_pawn_moves,
                "attacks": black_pawn_attacks
            }
        },
        "knight": knight_lookup,
        "king": king_lookup,
        "rook": {
            "masks": rook_masks,
            "moves": rook_moves
        },
        "bishop": {
            "masks": bishop_masks,
            "moves": bishop_moves
        }
    }

    # Guardar en un archivo JSON
    save_moves_to_json(precomputed_moves)
    print("Move database generated successfully!")
