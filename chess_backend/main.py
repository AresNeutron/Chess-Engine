import pygame
from chess_backend.app.final_filter import final_filter
from chess_backend.game_config import (
    draw_board, draw_pieces, draw_valid_moves, get_square_from_mouse, WIDTH, HEIGHT, draw_reset_button
)
from chess_backend.app.data.positions import load_positions_from_json
from chess_backend.app.game_state import make_move, reset_game

# Variables de estado
is_whites_turn = True
selected_piece = None
valid_moves = set()

# Crear la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

def handle_click(pos):
    """Maneja el clic del jugador para seleccionar piezas y mover."""
    global selected_piece, valid_moves, is_whites_turn
    piece_positions = load_positions_from_json()
    board_pos = get_square_from_mouse(pos)
    
    if board_pos is None:
        return
    
    # Si hay una pieza seleccionada, intentar mover
    if selected_piece and board_pos in valid_moves:
        make_move(board_pos, selected_piece)
        selected_piece = None
        valid_moves = set()
        is_whites_turn = not is_whites_turn
        return
    
    # Seleccionar nueva pieza
    for piece, position in piece_positions.items():
        if position == board_pos:
            piece_color = "white" if "white" in piece else "black"
            if (is_whites_turn and piece_color == "white") or \
               (not is_whites_turn and piece_color == "black"):
                selected_piece = piece
                valid_moves = set(final_filter(piece))
                return
    
    selected_piece = None
    valid_moves = set()

def main():
    """Bucle principal del juego."""
    clock = pygame.time.Clock()
    running = True
    
    while running:
        screen.fill("white")
        draw_board(screen)
        draw_pieces(screen)
        draw_valid_moves(valid_moves, screen)
        
        # Dibuja el botón de reinicio y obtén su rectángulo
        button_rect = draw_reset_button(screen)
        
        pygame.display.flip()
        clock.tick(5)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verifica si el clic fue en el botón de reinicio
                if button_rect[0] <= event.pos[0] <= button_rect[0] + button_rect[2] and \
                   button_rect[1] <= event.pos[1] <= button_rect[1] + button_rect[3]:
                    reset_game()  # Llama a la función de reinicio
                    global is_whites_turn
                    is_whites_turn = True
                else:
                    handle_click(event.pos)  # Maneja el clic en el tablero
    
    pygame.quit()

if __name__ == "__main__":
    main()