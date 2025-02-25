Chess Game with Backend Logic
This is a demo of a full-stack chess game project built from the ground up. Every component, from the user interface to the backend server and API, has been carefully designed and developed from scratch. The project provides a fully functional chessboard with implemented game logic, including special moves like castling and pawn promotion.

Note: This project is a prototype (MVP). While fully functional with all game logic implemented, it's not yet polished or production-ready.

Features
Interactive Chessboard
Click-and-move functionality.
Real-time visual indicators for valid moves.

Backend-Powered Game Logic
Built using Python and FastAPI.
The backend dynamically calculates all possible moves for each piece and ensures strict adherence to chess rules.
Robust update-moves function tracks valid moves in real time.
King safety verification: automatic detection and enforcement of moves to escape check.
Handles special rules like castling, pawn promotion, and en passant.

Database Integration
The backend uses SQLite for data storage.
Chess pieces are stored with fields such as name, position, hasMoved, and moves.
Python scripts initialize the database with all pieces in their starting positions on game setup.

API
RESTful API endpoints under /api for retrieving and updating game state.
Enables seamless communication between the frontend and backend.

How It Works

Backend Initialization
On server start, the database is cleared and repopulated with the initial chessboard configuration.
The backend dynamically calculates all possible moves for each piece and updates them in real time.

Frontend Integration
Players interact with a fully responsive React-based UI.
Piece movements are validated via API calls to ensure adherence to chess rules.

Game Flow
Pieces move only between valid positions.
Check and checkmate detection ensures game integrity.

Future Enhancements
Implement AI-powered opponents for single-player games.
Improve the UI to make the experience more enjoyable and visually appealing.
Implement logic to track movements, maintain player scores, and record victories and defeats.

Acknowledgments
This project was built entirely from scratch, showcasing custom-built algorithms, API design, and backend development.
