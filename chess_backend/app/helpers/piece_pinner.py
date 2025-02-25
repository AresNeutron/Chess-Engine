def get_pinned_pieces(king_name: str, piece_positions: dict, white_bitboard, black_bitboard):
    """ Detects pinned pieces that cannot move freely because they are protecting the king. """
    
    king_position = piece_positions[king_name]
    is_white = king_name.startswith("white")

    pinned_pieces = {}

    ray_directions = generate_ray_directions(king_position)

    for direction, ray in ray_directions.items():
        ally_found = None
        for square in ray:
            if (1 << square) & (white_bitboard if is_white else black_bitboard):  # Ally piece
                if ally_found is None:
                    ally_found = square  # First ally found
                else:
                    break  # Second ally found, no pin possible
            
            elif (1 << square) & (black_bitboard if is_white else white_bitboard):  # Enemy piece
                if ally_found is not None and is_valid_pin(direction, piece_positions, square):
                    pinned_pieces[ally_found] = list_to_bitboard(ray)  # Store pinned piece and its movement ray
                break  # Stop after finding an enemy

    return pinned_pieces


def generate_ray_directions(king_position):
    """
    Generates ray paths in all 8 directions from the king's position.
    Uses precomputed attack masks for efficiency.
    """
    directions = {
        "north": [], "south": [], "east": [], "west": [],
        "northeast": [], "northwest": [], "southeast": [], "southwest": []
    }
    
    rank, file = divmod(king_position, 8)  # Get row and column (0-7)
    
    for i in range(1, 8):
        if rank + i < 8: directions["north"].append((rank + i) * 8 + file)
        if rank - i >= 0: directions["south"].append((rank - i) * 8 + file)
        if file + i < 8: directions["east"].append(rank * 8 + (file + i))
        if file - i >= 0: directions["west"].append(rank * 8 + (file - i))
        
        if rank + i < 8 and file + i < 8: directions["northeast"].append((rank + i) * 8 + (file + i))
        if rank + i < 8 and file - i >= 0: directions["northwest"].append((rank + i) * 8 + (file - i))
        if rank - i >= 0 and file + i < 8: directions["southeast"].append((rank - i) * 8 + (file + i))
        if rank - i >= 0 and file - i >= 0: directions["southwest"].append((rank - i) * 8 + (file - i))
    
    return directions


def is_valid_pin(direction, piece_positions, enemy_square):
    """
    Checks if an enemy piece found in the ray direction can actually attack along that ray.
    """
    enemy_piece = None
    for name, pos in piece_positions.items():
        if pos == enemy_square:
            enemy_piece = name.split("-")[1]  # Extract piece type
            break  # Found the piece, exit loop immediately

    if enemy_piece is None:
        return False  # This should never happen, but a safety check

    if direction in ["north", "south", "east", "west"]:
        return enemy_piece in ["rook", "queen"]
    if direction in ["northeast", "northwest", "southeast", "southwest"]:
        return enemy_piece in ["bishop", "queen"]

    return False

def list_to_bitboard(squares):
    """Converts a list of squares (integers) to a bitboard."""
    bitboard = 0
    for square in squares:
        bitboard |= (1 << square)
    return bitboard