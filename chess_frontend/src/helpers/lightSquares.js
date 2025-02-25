import fetchBoards from "../endpoints/fetchBoards";
import boardArray from "../helpers/boardArray";

const lightSquares = async (piece_name, position, moves) => {
  // Crear una copia del tablero
  const newBoard = boardArray.slice();

  // Marcar la posición actual de la pieza en amarillo
  newBoard[position] = "yellow";

  // Obtener los bitboards, el endpoint devuelve una tupla que es convertida en array
  const bitboards = await fetchBoards();

  // Determinar si la pieza es blanca y seleccionar el bitboard enemigo
  const is_white = piece_name.includes("white");

  // El array contiene los tableros blanco y negro en ese orden
  let enemy_bitboard = is_white ? bitboards[1] : bitboards[0];

  // Convertir enemy_bitboard a BigInt si no lo es
  enemy_bitboard = BigInt(enemy_bitboard);

  // Recorrer los movimientos y marcar las casillas correspondientes
  moves.forEach((square) => {
    let bitMask = 1n << BigInt(square);

    // Verifica si la casilla tiene una pieza enemiga comparando BigInts
    if ((enemy_bitboard & bitMask) !== 0n) {
      newBoard[square] = "red"; // Pieza enemiga
    } else {
      newBoard[square] = "blue"; // Casilla vacía
    }
  });

  return newBoard;
};

export default lightSquares;
