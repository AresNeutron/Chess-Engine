from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from chess_backend.app.final_filter import final_filter
from chess_backend.app.data.positions import load_positions_from_json
from chess_backend.app.game_state import make_move, reset_game 
from chess_backend.app.data.board import load_boards
from chess_backend.app.helpers.checkers import is_king_in_check, is_promotion

app = FastAPI()

# Middleware CORS para permitir el acceso desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Almacenar conexiones WebSocket activas
active_connections: List[WebSocket] = []

async def notify_clients(event: str, data: dict):
    """Enviar notificaciones en tiempo real a los clientes conectados."""
    for connection in active_connections:
        await connection.send_json({"event": event, "data": data})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Manejar conexiones WebSocket con el frontend."""
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            message = await websocket.receive_json()  # Recibir mensajes JSON
            event = message.get("event")
            data = message.get("data")

            if event == "move":
                await process_move(data, websocket)

    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def process_move(data, websocket):
    """Procesar movimientos de piezas recibidos por WebSocket."""
    piece_name = data.get("piece_name")
    to_pos = data.get("to_pos")

    piece_positions = load_positions_from_json()
    
    if piece_name not in piece_positions:
        await websocket.send_json({"event": "error", "data": {"message": "Pieza no encontrada"}})
        return

    valid_moves = final_filter(piece_name)
    if to_pos not in valid_moves:
        await websocket.send_json({"event": "error", "data": {"message": "Movimiento inválido"}})
        return

    # Realizar el movimiento
    make_move(to_pos, piece_name)

    # Verificar promoción
    if is_promotion(to_pos, piece_name):
        await notify_clients("promotion_required", {"pawn": piece_name})

    # Verificar jaque
    if is_king_in_check(f"{piece_name[:5]}-king"):
        await notify_clients("check_alert", {"message": f"{piece_name[:5]}-king is in check"})

    # # Verificar jaque mate
    # if check_checkmate():
    #     await notify_clients("checkmate_alert", {"message": "Jaque mate. Fin del juego."})

    await notify_clients("move_made", {"piece": piece_name, "position": to_pos})

@app.get("/boards")
def get_boards():
    return load_boards()

@app.get("/pieces/")
def get_pieces():
    return load_positions_from_json()

@app.post("/reset/")
def reset():
    reset_game()
    return {"message": "Juego reiniciado"}

