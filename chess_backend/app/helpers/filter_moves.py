# In fact, this is a helper for the real filter
def _filter_moves(piece_name, position, precomputed_moves, white_bitboard, black_bitboard):
    """
    Efficiently filter precomputed moves for sliding pieces using bitwise operations.
    """
    piece_type = piece_name.split("-")[1]
    is_white = piece_name.startswith("white")
    
    # Get occupied squares
    occupied_squares = white_bitboard | black_bitboard
    moves_bitboard = 0
    
    if piece_type == "pawn":
        moves_bitboard = helper_for_pawn(is_white, position, precomputed_moves, white_bitboard, black_bitboard)

    elif piece_type in ["bishop", "rook"]:
        moves_bitboard = helper_for_rbq(piece_type, position, precomputed_moves, occupied_squares)
    
    elif piece_type == "queen":
        linear_moves = helper_for_rbq("rook", position, precomputed_moves, occupied_squares)
        diagonal_moves = helper_for_rbq("bishop", position, precomputed_moves, occupied_squares)
        moves_bitboard = linear_moves | diagonal_moves

    # For king and knight
    else:
        moves_bitboard = precomputed_moves[piece_type].get(str(position), 0)

    # Remove friendly occupied squares (can't capture own pieces)
    friendly_bitboard = white_bitboard if is_white else black_bitboard
    moves_bitboard &= ~friendly_bitboard

    return moves_bitboard


def helper_for_rbq(piece_type, position, precomputed_moves, occupied_squares):
    mask = precomputed_moves[piece_type]["masks"].get(str(position), 0)

    index = occupied_squares & mask
    moves = precomputed_moves[piece_type]["moves"].get(str(position), 0).get(str(index), 0)

    return moves


def helper_for_pawn(is_white, position, precomputed_moves, white_bitboard, black_bitboard):
    # Get the precomputed moves for the piece at the given position
    color = "white" if is_white else "black"
    moves_bitboard = precomputed_moves["pawn"][color]["moves"].get(str(position), 0)
    attacks_bitboard = precomputed_moves["pawn"][color]["attacks"].get(str(position), 0)
        
    # Combine the bitboards to get all occupied squares
    occupied_squares = white_bitboard | black_bitboard

    # Get the enemy bitboard    
    enemy_bitboard = black_bitboard if is_white else white_bitboard

    # Filter the moves wiht occupied squares
    filtered_moves = moves_bitboard & ~occupied_squares

    cant_move_forward = is_white and (occupied_squares >> (position + 8)) & 1
    cant_move_backward = not is_white and (occupied_squares >> (position - 8)) & 1
    
    if cant_move_forward or cant_move_backward:
        filtered_moves = 0

    # Filter moves based on piece type
    filtered_attacks = attacks_bitboard & enemy_bitboard

    return filtered_moves | filtered_attacks