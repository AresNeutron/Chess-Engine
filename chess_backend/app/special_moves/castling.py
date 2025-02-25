castling_rights = 0b1111

# Bit 0: White king-side castling
# Bit 1: White queen-side castling
# Bit 2: Black king-side castling
# Bit 3: Black queen-side castling

# To check if the king's moves during castling are safe
castling_map = {
    "white-rook-1": 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00001110, # The rook far from the king 
    "white-rook-2": 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_01100000, # The rook close to the king
    "black-rook-1": 0b00001110_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
    "black-rook-2": 0b01100000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
}

castling_masks = {
    "white-king": 0b1100,
    "white-rook-1": 0b1101, # The rook far from the king 
    "white-rook-2": 0b1110, # The rook close to the king
    "black-king": 0b0011,
    "black-rook-1": 0b0111,
    "black-rook-2": 0b1011
    }
 
# This function will be called after every move
def update_castling_rights(piece_name):
    global castling_rights

    if piece_name in castling_masks.keys():
        castling_rights &= castling_masks[piece_name]


def reset_castling_rights():
    global castling_rights
    castling_rights = 0b1111


def can_castle(king_name: str, piece_positions: dict, enemy_attack_map, white_bitboard, black_bitboard):
    """ Verifica si el enroque es posible para ambos lados. """
    global castling_rights
    
    is_white = king_name.startswith("white")
    king_position = piece_positions[king_name]
    
    rook_king_side = f"{'white' if is_white else 'black'}-rook-2"
    rook_queen_side = f"{'white' if is_white else 'black'}-rook-1"
    occupied_board = black_bitboard | white_bitboard
    castling_bitboard = 0
    
    for rook in [rook_king_side, rook_queen_side]:
        if rook not in piece_positions:
            continue
        
        rook_position = piece_positions[rook]
        castling_mask = castling_map[rook]
        
        is_path_clear = (castling_mask & occupied_board) == 0
        have_not_moved = bool(castling_rights & castling_masks[rook])
        kings_path = castling_mask | (1 << king_position)
        is_castling_safe = (enemy_attack_map & kings_path) == 0
        
        if is_path_clear and have_not_moved and is_castling_safe:
            castling_bitboard |= (1 << rook_position)
    
    return castling_bitboard
