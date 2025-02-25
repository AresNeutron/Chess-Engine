from chess_backend.app.helpers.filter_moves import _filter_moves
from chess_backend.app.special_moves.castling import can_castle

# This function is superior to _filter_moves
def get_enemy_attack_map(king_name: str, piece_positions: dict, precomputed_moves,
                      white_bitboard, black_bitboard):
    enemy_attack_map = 0
    is_white = king_name.startswith("white")

    # Identify enemy pieces
    enemy_pieces = {k: v for k, v in piece_positions.items() if k.startswith("black" if is_white else "white")}

    # Compute attack map
    for piece_name, position in enemy_pieces.items():
        attack_bitboard = _filter_moves(piece_name, position, precomputed_moves, white_bitboard, black_bitboard)
        enemy_attack_map |= attack_bitboard

    # Check if the king is under attack
    return enemy_attack_map


def filter_king_moves(king_name: str, piece_positions: dict, precomputed_moves,
                      white_bitboard, black_bitboard):
    king_position = piece_positions[king_name]
    king_moves = _filter_moves(king_name, king_position, precomputed_moves, white_bitboard, black_bitboard)
    enemy_attack_map = get_enemy_attack_map(king_name, piece_positions, precomputed_moves,
                      white_bitboard, black_bitboard)
    
    # Check if king can castle
    castling_bitboard = can_castle(king_name, piece_positions, enemy_attack_map, white_bitboard, black_bitboard)
    king_moves |= castling_bitboard

    # Return the safe moves for the king
    return (king_moves & ~enemy_attack_map)
