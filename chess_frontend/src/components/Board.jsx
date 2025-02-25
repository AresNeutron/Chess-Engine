import { useChessContext } from "../hooks/ChessContext";
import boardArray from "../helpers/boardArray";
import Pieces from "./Pieces";
import Square from "./Square";

function Board() {
  const { lighted } = useChessContext();

  return (
    <div className="board">
      {/*Adding the 64 squares. Since this won't change we can use boardArray */}
      {boardArray.map((square, index) => {
          const isBlack = Math.floor(index / 8) % 2 === index % 2; // Alternate color
          const isBlue = lighted[index] === "blue";
          const isRed = lighted[index] === "red";
          const isYellow = lighted[index] === "yellow";
          const isViolet = lighted[index] === "violet";
          return (
            <div
              key={index}
              className="boardCell"
              style={{
                backgroundColor: isBlack ? "#6e8a3a" : "#aad751", // Chessboard colors
              }}
            >
              {lighted[index] ? (
                <Square
                // se le resta el index a 64 para invertir las posiciones
                // los bitboards estan ordenados de abajo hacia arriba, al inverso del
                // renderizado de las casillas
                  position = {index}
                  blue={isBlue}
                  yellow={isYellow}
                  red={isRed}
                  violet={isViolet}
                />
              ) :
              square}
            </div>
          );
        })
      }
      <Pieces/>
    </div>
  );
}

export default Board;
