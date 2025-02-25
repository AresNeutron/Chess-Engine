import json
import os
from hashlib import sha256

# Get the absolute path of the JSON file
folder_name = "game_recordings"

class MoveTracker:
    def __init__(self, game_id):
        self.history = []  # Lista de movimientos
        self.position_counts = {}  # Conteo de posiciones
        self.turn = 1
        self.current_player = "white"
        
        self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), folder_name, f"{game_id}.json"))
        
        # Crear el archivo JSON si no existe
        if not os.path.exists(self.file_path):
            self.save_to_json()
        else:
            self.load_from_json()
    
    def hash_position(self, white_bb, black_bb):
        """Genera un hash único para la posición basada en los bitboards."""
        position_str = f"{white_bb}_{black_bb}"
        return sha256(position_str.encode()).hexdigest()
    
    def record_move(self, piece_name, white_bb, black_bb):
        """Registra un movimiento en la historia y actualiza la cuenta de posiciones."""
        position_hash = self.hash_position(white_bb, black_bb)
        
        # Actualizar el conteo de la posición
        if position_hash in self.position_counts:
            self.position_counts[position_hash] += 1
        else:
            self.position_counts[position_hash] = 1
        
        change = 0 # Bitboard para guardar el cambio en el tablero

        if self.history:  # There must be at least one recording
            last_turn_record = self.history[-1]

            # The bitboard of the current player as it was the last turn
            last_bitboard = last_turn_record["bitboards"][self.current_player]
            current_bitboard = white_bb if self.current_player == "white" else black_bb
            change = current_bitboard ^ last_bitboard # Store the change 

        # Registrar el movimiento
        self.history.append({
            "turn": self.turn,
            "player": self.current_player,
            "moved_piece": piece_name,
            "change": change,
            "bitboards": {
                "white": white_bb,
                "black": black_bb
            },
            "hash": position_hash,
            "count": self.position_counts[position_hash]
        })
        
        # Alternar jugador y aumentar el turno
        self.current_player = "black" if self.current_player == "white" else "white"
        self.turn += 1
    
    def save_to_json(self):
        """Guarda el historial en un archivo JSON."""
        with open(self.file_path, "w") as f:
            json.dump({"history": self.history, "position_counts": self.position_counts}, f, indent=4)
    
    def load_from_json(self):
        """Carga el historial desde un archivo JSON. Si no existe, lo crea."""
        if not os.path.exists(self.file_path):
            self.save_to_json()
        else:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                self.history = data["history"]
                self.position_counts = data["position_counts"]
                
                # Restaurar el turno y jugador actual
                if self.history:
                    last_move = self.history[-1]
                    self.turn = last_move["turn"] + 1
                    self.current_player = "black" if last_move["player"] == "white" else "white"


def update_recordings(piece_name, white_bitboard, black_bitboard):
    # The MoveTracker requires an id parameter, but let's use the same for now
    move_tracker = MoveTracker("test")
    move_tracker.load_from_json()
    move_tracker.record_move(piece_name, white_bitboard, black_bitboard)
    move_tracker.save_to_json()