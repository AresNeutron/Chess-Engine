from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from chess_backend.app.final_filter import final_filter
from chess_backend.app.data.positions import load_positions_from_json
from chess_backend.app.game_state import make_move
from chess_backend.app.helpers.checkers import is_movement_check, is_promotion
from chess_backend.routes import router  # Importamos el nuevo router

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregamos las rutas HTTP
app.include_router(router)

# WebSockets: Almacenar conexiones activas
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
            message: dict = await websocket.receive_json()  # Recibir mensajes JSON
            event = message.get("event")
            data = message.get("data")

            if event == "move":
                await process_move(data, websocket)

    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def process_move(data: dict, websocket: WebSocket):
    """Procesar movimientos de piezas recibidos por WebSocket."""
    piece_name: str = data.get("piece_name")
    to_pos = data.get("to_pos")

    piece_positions = load_positions_from_json()
    is_white = piece_name.startswith("white")
    
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
    enemy_king = f"{"black" if is_white else "white"}-king"
    if is_movement_check(enemy_king): # This one is the enemy king
        await notify_clients("check_alert", {"message": f"{enemy_king} is in check"})
    
     # # Verificar jaque mate
    # if check_checkmate():
    #     await notify_clients("checkmate_alert", {"message": "Jaque mate. Fin del juego."})

    await notify_clients("move_made", {"piece": piece_name, "position": to_pos})
