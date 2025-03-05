import { useState } from "react";
import "./App.css";
import Board from "./components/Board";
import { useChessContext } from "./hooks/ChessContext";
import useWebSocket from "./hooks/useWebSockets";

function App() {
  const [promotion, setPromotion] = useState(null);
  const [checkMessage, setCheckMessage] = useState("");
  const [checkmateMessage, setCheckmateMessage] = useState("");

  const handleReset = async () => {
    if (window.confirm("Are you sure you want to reset the game?")) {
      resetState()
    }
  };

  const { whitesTurn, resetState} = useChessContext();

  return (
    <div className="App">
      <div className="info">
        <h1>Welcome to my awesome Chess Titans Clone</h1>
        <div>
          <h2>{whitesTurn ? "White" : "Black"}'s Turn</h2>
          <button className="resetButton" onClick={handleReset}>
            Restart
          </button>
        </div>
      </div>
      {/* {isPromoting && <Promote isWhite={isWhitePromotion}/>} */}
      <Board />
    </div>
  )
}

export default App
