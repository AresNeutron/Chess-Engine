import pygame
import os
from chess_backend.app.data.positions import load_positions_from_json

# Obtener la ruta de la carpeta de imágenes
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "images"))

WIDTH, HEIGHT = 800, 600
BOARD_SIZE = 480
SQUARE_SIZE = BOARD_SIZE // 8
MARGIN_X = (WIDTH - BOARD_SIZE) // 2
MARGIN_Y = (HEIGHT - BOARD_SIZE) // 2

# Colores
LIGHT_GREEN = (170, 215, 81)
DARK_GREEN = (110, 138, 58)
HIGHLIGHT_COLOR = (255, 255, 255, 200)  # Blanco semi-transparente

# Inicializar pygame y sus módulos
pygame.init()
pygame.font.init()

# Fuente para la nomenclatura
FONT = pygame.font.Font(None, 24)

# Cargar imágenes de las piezas y redimensionarlas
IMAGES = {}
pieces = [
    "black-bishop", "black-king", "black-knight", "black-pawn",
    "black-queen", "black-rook", "white-bishop", "white-king",
    "white-knight", "white-pawn", "white-queen", "white-rook"
]
for piece in pieces:
    path = os.path.join(folder_path, f"{piece}.png")
    img = pygame.image.load(path)
    IMAGES[piece] = pygame.transform.smoothscale(img, (SQUARE_SIZE, SQUARE_SIZE))


def draw_board(screen):
    """Dibuja el tablero con casillas alternando colores."""
    for row in range(8):
        for col in range(8):
            color = LIGHT_GREEN if (row + col) % 2 == 0 else DARK_GREEN
            pygame.draw.rect(screen, color, (MARGIN_X + col * SQUARE_SIZE, MARGIN_Y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    # Dibujar la nomenclatura
    for i in range(8):
        letter = chr(65 + i)  # A-H
        number = str(8 - i)  # 8-1
        text_surface = FONT.render(letter, True, "black")
        screen.blit(text_surface, (MARGIN_X + i * SQUARE_SIZE + SQUARE_SIZE // 2 - 6, MARGIN_Y - 20))
        screen.blit(text_surface, (MARGIN_X + i * SQUARE_SIZE + SQUARE_SIZE // 2 - 6, MARGIN_Y + BOARD_SIZE + 5))
        text_surface = FONT.render(number, True, "black")
        screen.blit(text_surface, (MARGIN_X - 20, MARGIN_Y + i * SQUARE_SIZE + SQUARE_SIZE // 2 - 6))
        screen.blit(text_surface, (MARGIN_X + BOARD_SIZE + 5, MARGIN_Y + i * SQUARE_SIZE + SQUARE_SIZE // 2 - 6))


def draw_pieces(screen):
    """Dibuja las piezas en sus posiciones."""
    piece_positions = load_positions_from_json()

    for piece, position in piece_positions.items():
        row, col = 7 - (position // 8), position % 8
        piece_name = "-".join(piece.split("-")[:2])
        if piece_name in IMAGES:
            screen.blit(IMAGES[piece_name], (MARGIN_X + col * SQUARE_SIZE, MARGIN_Y + row * SQUARE_SIZE))


def draw_valid_moves(valid_moves, screen):
    """Dibuja círculos en los movimientos válidos."""
    for move in valid_moves:
        row, col = 7 - (move // 8), move % 8
        center = (MARGIN_X + col * SQUARE_SIZE + SQUARE_SIZE // 2, MARGIN_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2)
        pygame.draw.circle(screen, HIGHLIGHT_COLOR, center, SQUARE_SIZE // 6)


def get_square_from_mouse(pos):
    """Convierte la posición del mouse en una casilla del tablero."""
    x, y = pos
    col = (x - MARGIN_X) // SQUARE_SIZE
    row = (y - MARGIN_Y) // SQUARE_SIZE
    if 0 <= col < 8 and 0 <= row < 8:
        return (7 - row) * 8 + col
    return None


def draw_reset_button(screen):
    """Dibuja un botón de reinicio en la pantalla."""
    button_width, button_height = 120, 40
    button_x = WIDTH - button_width - 20  # 20px from the right edge
    button_y = 20  # 20px from the top edge

    # Dibuja el rectángulo del botón
    pygame.draw.rect(screen, (200, 50, 50), (button_x, button_y, button_width, button_height))

    # Dibuja el texto del botón
    font = pygame.font.Font(None, 30)
    text_surface = font.render("Reset Game", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text_surface, text_rect)

    return (button_x, button_y, button_width, button_height)