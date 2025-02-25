import { useChessContext } from "../hooks/ChessContext";

//This component only renders if its position is lighted
function Square({
  position,
  blue = false,
  yellow = false,
  red = false,
  violet = false,
}) {
  const { selectedPiece, handleMoveState} = useChessContext();
  
  return (
    <div
      onClick={() => {
        if (selectedPiece)  handleMoveState(position, selectedPiece);
      }}
      className={`square ${blue && "blue"} ${violet && "violet"} ${
        red && "red"
      } ${yellow && "yellow"}`}
    ></div>
  );
  };

export default Square;
