from chess_backend.app.data.board import load_boards, store_boards, reset_boards
from chess_backend.app.data.positions import load_positions_from_json, save_positions_to_json, reset_positions
from chess_backend.app.data.pins import store_pinned_pieces, reset_pinned_pieces
from chess_backend.app.data.move_tracker import update_recordings
from chess_backend.app.helpers.move_helper_functions import make_castling, make_en_passant, make_normal_move
from chess_backend.app.special_moves.castling import update_castling_rights, reset_castling_rights

def make_move(to_pos: int, piece_name: str):
    """ Realiza un movimiento y actualiza el estado del juego.
    Maneja movimientos normales, en passant, enroque y coronación. """
    piece_positions = load_positions_from_json()
    white_bitboard, black_bitboard = load_boards()

    is_white = piece_name.startswith("white")
    ally_board = white_bitboard if is_white else black_bitboard
    enemy_board = black_bitboard if is_white else white_bitboard
    from_pos = piece_positions[piece_name]

    is_king_castling = (is_white and to_pos in [0, 7]) or (not is_white and to_pos in [56, 63])

    if "king" in piece_name and is_king_castling:
        piece_positions, ally_board = make_castling(to_pos, piece_name, piece_positions, ally_board)

    elif "pawn" in piece_name:
        if abs((to_pos % 8) - (from_pos % 8)) == 1 and not (enemy_board >> to_pos & 1):
            piece_positions, ally_board, enemy_board = make_en_passant(to_pos, piece_name, piece_positions, ally_board, enemy_board)
        
        else:
            piece_positions, ally_board, enemy_board = make_normal_move(to_pos, piece_name, piece_positions, ally_board, enemy_board)
    else:
        piece_positions, ally_board, enemy_board = make_normal_move(to_pos, piece_name, piece_positions, ally_board, enemy_board)
    
    if is_white:
        white_bitboard = ally_board
        black_bitboard = enemy_board
    else:
        black_bitboard = ally_board
        white_bitboard = enemy_board
    
    update_castling_rights(piece_name)
    store_boards(white_bitboard, black_bitboard)
    save_positions_to_json(piece_positions)
    store_pinned_pieces(piece_positions, white_bitboard, black_bitboard)
    update_recordings(piece_name, white_bitboard, black_bitboard)


def reset_game():
    reset_boards()
    reset_positions()

    # This one must be called after reset_positions()
    reset_pinned_pieces()
    
    # Global variables must also be reset
    reset_castling_rights()