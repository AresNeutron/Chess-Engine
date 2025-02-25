import blackBishop from "../images/black-bishop.png";
import blackKnight from "../images/black-knight.png";
import blackPawn from "../images/black-pawn.png";
import blackRook from "../images/black-rook.png";
import blackKing from "../images/black-king.png";
import blackQueen from "../images/black-queen.png";
import whiteQueen from "../images/white-queen.png";
import whitePawn from "../images/white-pawn.png";
import whiteKing from "../images/white-king.png";
import whiteBishop from "../images/white-bishop.png";
import whiteRook from "../images/white-rook.png";
import whiteKnight from "../images/white-knight.png";

// Map piece names to imported images
export const pieceImages = {
  "black-bishop": blackBishop,
  "black-knight": blackKnight,
  "black-pawn": blackPawn,
  "black-rook": blackRook,
  "black-king": blackKing,
  "black-queen": blackQueen,
  "white-queen": whiteQueen,
  "white-pawn": whitePawn,
  "white-king": whiteKing,
  "white-bishop": whiteBishop,
  "white-rook": whiteRook,
  "white-knight": whiteKnight,
};

export const clearString = (piece_name) => {
  // The king has no index
  if (piece_name.includes("king")) return piece_name

  // Return the piece without the index
  const parts = piece_name.split("-");
  parts.pop(); 
  return parts.join("-"); 
};