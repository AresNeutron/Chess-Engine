from chess_backend.app.helpers.filter_moves import _filter_moves
from chess_backend.app.data.moves import load_moves_from_json
from chess_backend.app.data.positions import load_positions_from_json
from chess_backend.app.data.board import load_boards
from chess_backend.app.helpers.filter_for_king import filter_king_moves
from chess_backend.app.data.pins import load_pinned_pieces
from chess_backend.app.special_moves.en_passant import can_en_passant

# This filter returns the moves considering the check and everything else
def final_filter(piece_name: str):
    # Load all necesary variables
    precomputed_moves = load_moves_from_json()
    piece_positions = load_positions_from_json()
    position = piece_positions[piece_name]
    white_bitboard, black_bitboard = load_boards()
    white_pins, black_pins = load_pinned_pieces()
    
    is_white = piece_name.startswith("white")
    moves = 0
    current_pins: dict = white_pins if is_white else black_pins

    if "king" in piece_name:
        moves = filter_king_moves(piece_name, piece_positions, precomputed_moves, white_bitboard, black_bitboard)
    else:
        moves = _filter_moves(piece_name, position, precomputed_moves, white_bitboard, black_bitboard)
        
        if "pawn" in piece_name: # For en-passant
            en_passant_bitboard = can_en_passant(piece_name, piece_positions)
            moves |= en_passant_bitboard

        # This fiters the moves if the piece is pinned
        if str(position) in current_pins.keys():
            ray = current_pins[str(position)]
            moves &= ray

    # Thin converts the bitboards to a list of positions as integers from 0 to 63
    moves = bitboard_to_positions(moves)
    print(moves)

    return moves


def bitboard_to_positions(bitboard: int) -> list[int]:
    positions = []
    position = 0
    
    while bitboard:
        if bitboard & 1:
            positions.append(position)
        bitboard >>= 1
        position += 1
        
    return positions