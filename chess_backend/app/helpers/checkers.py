from chess_backend.app.helpers.filter_for_king import get_enemy_attack_map
from chess_backend.app.data.board import load_boards
from chess_backend.app.data.moves import load_moves_from_json
from chess_backend.app.data.positions import load_positions_from_json

def is_promotion(to_pos: int, pawn_name: str):
    """Verifica si un peón ha alcanzado la última fila para promoción."""
    row = to_pos // 8  # Obtener la fila en base a la posición

    if ("white" in pawn_name and row == 7) or ("black" in pawn_name and row == 0):
        return True  # Se debe realizar una promoción
    return False  # No necesita promoción


def is_king_in_check(king_name: str):
    piece_positions = load_positions_from_json()
    white_bitboard, black_bitboard = load_boards()
    precomputed_moves = load_moves_from_json()

    king_position = piece_positions[king_name]
    enemy_attack_map = get_enemy_attack_map(king_name, piece_positions, precomputed_moves,
                      white_bitboard, black_bitboard)
    
    # Check if the king is under attack
    return bool(enemy_attack_map & (1 << king_position))