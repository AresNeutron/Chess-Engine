import { createContext, useContext, useEffect, useRef, useState } from "react";
import boardArray from "../helpers/boardArray";
import fetchPieces from "../endpoints/fetchPieces";
import lightSquares from "../helpers/lightSquares";
import movePiece from "../endpoints/movePiece";
import getMoves from "../endpoints/getMoves";
import resetGame from "../endpoints/resetGame";
import useWebSocket from "./useWebSockets";

const ChessContext = createContext(undefined);

const ContextProvider = ({ children }) => { // ← Agregar children aquí
  const [whitesTurn, setWhitesTurn] = useState(true);
  const [data, setData] = useState({});
  const [lighted, setLighted] = useState(boardArray);
  const [selectedPiece, setSelectedPiece] = useState("");
  const socketRef = useRef(null)

   // WebSocket hook
   socketRef.current = useWebSocket((eventType, eventData) => {
    if (eventType === "move_made") {
      initializeData(); // Actualizamos el estado cuando se recibe un movimiento
    }
    if (eventType === "promotion_required") {
      console.log("¡Promoción requerida!", eventData);
    }
    if (eventType === "check_alert") {
      console.log("¡Jaque!", eventData);
    }
    if (eventType === "checkmate_alert") {
      console.log("¡Jaque mate!", eventData);
    }
  });

  const handleLightState = async (piece_name, position) => {
    const moves = await getMoves(piece_name);
    const newLighted = await lightSquares(piece_name, position, moves);
    setLighted(newLighted);
  };

  const handleMoveState = async (to_pos, piece_name) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(
        JSON.stringify({
          event: "move",
          data: { piece_name, to_pos },
        })
      );
    } else {
      console.error("WebSocket no está conectado");
    }
    setLighted(boardArray);
    setSelectedPiece("");
    setWhitesTurn(!whitesTurn);
  };

  const initializeData = async () => {
    const pieces = await fetchPieces();
    setData(pieces);
  };

  async function resetState() {
    await resetGame();
    await initializeData()  
    setLighted(boardArray);
    setSelectedPiece("");
    setWhitesTurn(true);
  }

  useEffect(() => {
    initializeData();
  }, []);

  return (
    <ChessContext.Provider
      value={{
        whitesTurn,
        data,
        setData,
        lighted,
        handleLightState,
        selectedPiece,
        setSelectedPiece,
        handleMoveState,
        initializeData,
        resetState
      }}
    >
      {children} {/* ← Se debe renderizar children aquí */}
    </ChessContext.Provider>
  );
};

export default ContextProvider;

export const useChessContext = () => {
  const context = useContext(ChessContext);
  if (!context) {
    throw new Error("Must be used within a AppContext Provider");
  }
  return context;
};
