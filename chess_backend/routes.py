from fastapi import APIRouter
from chess_backend.app.data.positions import load_positions_from_json
from chess_backend.app.game_state import reset_game
from chess_backend.app.data.board import load_boards
from chess_backend.app.final_filter import final_filter

router = APIRouter()

@router.get("/boards")
def get_boards():
    return load_boards()

@router.get("/pieces/")
def get_pieces():
    return load_positions_from_json()

@router.post("/reset/")
def reset():
    reset_game()
    return {"message": "Juego reiniciado"}

@router.get("/valid-moves/{piece_name}")
def get_moves(piece_name: str):
    return {"valid_moves": final_filter(piece_name)}
