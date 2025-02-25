from chess_backend.app.data.move_tracker import MoveTracker

def can_en_passant(pawn_name: str, piece_positions):
    """Determina si un peón puede capturar al paso y devuelve el bitboard con la posición final."""
    
    # Bitboards que representan las casillas clave para en passant
    ENEMY_WHITE_TRACK = 0b00000000_00000000_00000000_00000000_11111111_00000000_11111111_00000000
    ENEMY_BLACK_TRACK = 0b00000000_11111111_00000000_11111111_00000000_00000000_00000000_00000000
    
    CURRENT_WHITE_TRACK = 0b00000000_00000000_00000000_11111111_00000000_00000000_00000000_00000000
    CURRENT_BLACK_TRACK = 0b00000000_00000000_00000000_00000000_11111111_00000000_00000000_00000000
    
    is_white = pawn_name.startswith("white")
    current_pos = piece_positions[pawn_name]
    current_track = CURRENT_WHITE_TRACK if is_white else CURRENT_BLACK_TRACK
    
    # Verificar si el peón está en la fila correcta para capturar al paso
    if not (current_track & (1 << current_pos)):
        return 0
    
    # Cargar el historial de movimientos
    move_tracker = MoveTracker("test")
    move_tracker.load_from_json()
    history = move_tracker.history
    if not history:
        return 0  # No hay movimientos previos
    
    last_record = history[-1]  # Último movimiento registrado
    last_change = last_record["change"]  # Posiciones que cambiaron en el tablero
    enemy_name = last_record["moved_piece"]
    enemy_track = ENEMY_BLACK_TRACK if is_white else ENEMY_WHITE_TRACK
    
    # Verificar si el último movimiento fue de un peón enemigo dentro del área de captura
    if "pawn" in enemy_name and (last_change & enemy_track) == last_change:
        enemy_pos = piece_positions[enemy_name]
        
        # Comprobar si el peón enemigo está en una columna adyacente
        if abs(enemy_pos - current_pos) == 1:
            final_pos = (enemy_pos + 8) if is_white else (enemy_pos - 8)
            return (1 << final_pos)  # Devuelve el bitboard con la posición de captura
    
    return 0
