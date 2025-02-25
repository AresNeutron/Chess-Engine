def make_castling(to_pos, king_name: str, piece_positions, ally_board):
    is_white = king_name.startswith("white")
    from_pos = piece_positions[king_name]

    rook_name, rook_from, rook_to, king_to = (
        ("white-rook-2", 7, 5, 6) if to_pos > from_pos else ("white-rook-1", 0, 3, 2)
    ) if is_white else (
        ("black-rook-2", 63, 61, 62) if to_pos > from_pos else ("black-rook-1", 56, 59, 58)
    )

    piece_positions[king_name] = king_to
    piece_positions[rook_name] = rook_to

    # Se limpian ambas posiciones originales del rey y la torre
    ally_board &= ~((1 << from_pos) | (1 << rook_from))
    ally_board |= (1 << king_to) | (1 << rook_to)

    return piece_positions, ally_board


def make_en_passant(to_pos: int, pawn_name: str, piece_positions, ally_board, enemy_board):
    is_white = pawn_name.startswith("white")

    captured_en_passant_pos = (to_pos - 8) if is_white else (to_pos + 8)

    # Eliminar la pieza enemiga (peón) que se captura en passant
    enemy_board &= ~(1 << captured_en_passant_pos)

    for enemy_piece, enemy_pos in list(piece_positions.items()):
        if (enemy_pos == captured_en_passant_pos and
            enemy_piece.startswith("black" if is_white else "white") and
            "pawn" in enemy_piece):
            del piece_positions[enemy_piece]
            break

    # Mover el peon hacia la casilla de destino
    piece_positions, ally_board, enemy_board = make_normal_move(to_pos, pawn_name,
                    piece_positions, ally_board, enemy_board)

    return piece_positions, ally_board, enemy_board


def make_promotion(to_pos: int, pawn_name: str, piece_positions: dict, ally_board, enemy_board):
    # Hacer el movimiento normalmente
    piece_positions, ally_board, enemy_board = make_normal_move(to_pos,
                    pawn_name, piece_positions, ally_board, enemy_board)

    # Por defecto se promueve a reina, ya veremos luego los demas
    new_piece_name = pawn_name.replace("pawn", "queen")

    # Actualizar piece_positions: cambiar la clave de la pieza
    piece_positions[new_piece_name] = piece_positions.pop(pawn_name)
    piece_name = new_piece_name

    return piece_positions, ally_board, piece_name


def make_normal_move(to_pos: int, piece_name: str, piece_positions, ally_board, enemy_board):
    is_white = piece_name.startswith("white")
    from_pos = piece_positions[piece_name]

    # Actualizar el tablero aliado: quitar de la casilla origen y agregar en la destino.
    ally_board &= ~(1 << from_pos)
    ally_board |= (1 << to_pos)
    piece_positions[piece_name] = to_pos

    # --- Manejar captura normal ---
    if enemy_board >> to_pos & 1:
        enemy_board &= ~(1 << to_pos)
        # Eliminar de piece_positions a la pieza enemiga capturada
        for enemy_piece, enemy_pos in list(piece_positions.items()):
            if enemy_pos == to_pos and enemy_piece.startswith("black" if is_white else "white"):
                del piece_positions[enemy_piece]
                break

    return piece_positions, ally_board, enemy_board