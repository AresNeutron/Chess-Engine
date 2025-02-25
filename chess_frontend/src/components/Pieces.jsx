import { useChessContext } from "../hooks/ChessContext";
import { clearString, pieceImages } from "../helpers/dataReferences";

function Pieces() {
  const {
    whitesTurn,
    data,
    lighted,
    selectedPiece,
    setSelectedPiece,
    handleLightState,
    handleMoveState
  } = useChessContext();
  const imageWidth = 64; //width set to the images

  function handleClick(piece_name, pos) {
    const is_white = piece_name.includes("white")

    if (selectedPiece) {
      // Para cambiar de pieza seleccionada
      if ((whitesTurn && is_white) || (!whitesTurn && !is_white)) {
        handleLightState(piece_name, pos);
        setSelectedPiece(piece_name);

      // Para capturar
      } else {
        if (lighted[pos]) handleMoveState(pos, selectedPiece)
      }
    } else {
      // Para seleccionar la pieza que se mueve
      if ((whitesTurn && is_white) || (!whitesTurn && !is_white)) {
        handleLightState(piece_name, pos);
        setSelectedPiece(piece_name);
      }
    }
  }

  return (
    <div className="pieceContainer">
      <div className='innerPieceContainer'>
        {/* Adding the pieces*/}
        {Object.keys(data).map((piece_name) => {
          const image = clearString(piece_name);

          // Las posiciones no estan invertidas
          const pos = data[piece_name]
          const col = pos % 8  // Columna
          const row = Math.floor(pos / 8) // Fila

          return (
            <div
              key={piece_name} // Important: Add a unique key prop
              onClick={() => {
                  handleClick(piece_name, pos)
                }
              }
              className="piece"
              style={{
                top: `${row * (imageWidth - 1)}px`,
                left: `${col * imageWidth - 1}px`,
              }}
            >
              <img src={pieceImages[image]} alt={piece_name} />
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Pieces;
