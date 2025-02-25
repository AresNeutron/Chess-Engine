from chess_backend.app.sliding_pieces.masks import generate_bishop_mask, generate_rook_mask
from chess_backend.app.sliding_pieces.blockers import generate_blocker_combinations

bishop_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
rook_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def generate_moves_bitboard(square, combination, directions):
    """Genera los movimientos posibles de una pieza considerando los bloqueadores."""
    rank = square // 8
    file = square % 8
    moves_bitboard = 0

    for dr, df in directions:  # Recorremos cada dirección válida
        r, f = rank, file

        while True:
            r += dr
            f += df

            if not (0 <= r < 8 and 0 <= f < 8):  # Si sale del tablero, detener la iteración
                break

            pos = r * 8 + f  # Convertir fila y columna en índice del bitboard
            moves_bitboard |= (1 << pos)  # Agregar casilla a los movimientos posibles

            if (combination >> pos) & 1:  # Si hay un bloqueador, detenerse en esta casilla
                break

    return moves_bitboard


def generate_sliding_moves():
    """Genera todos los bitboards de posibles movimientos para alfil y torre, considerando
    todas las combinaciones de obtaculos"""
    bishop_moves = {}
    bishop_masks = {}
    rook_moves = {}
    rook_masks = {}

    for square in range(64):
        # Generar las mascaras y almacenarlas, crear un diccionario para guardar movimientos
        b_mask = generate_bishop_mask(square)
        bishop_masks[square] = b_mask
        bishop_moves[square] = {}

        r_mask = generate_rook_mask(square)
        rook_masks[square] = r_mask
        rook_moves[square] = {}

        b_combinations = generate_blocker_combinations(b_mask)
        r_combinations = generate_blocker_combinations(r_mask)

        for combination in b_combinations:
            bishop_moves[square][combination] = generate_moves_bitboard(square, combination, bishop_directions)
        
        for combination in r_combinations:
            rook_moves[square][combination] = generate_moves_bitboard(square, combination, rook_directions)

    return bishop_masks, bishop_moves, rook_masks, rook_moves