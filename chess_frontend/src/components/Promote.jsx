import { useEffect, useState } from "react";
import { useChessContext } from "../hooks/ChessContext";
import { pieceImages } from "../helpers/dataReferences";

function Promote({ isWhite }) {
  const { initializeData, setIsPromoting } = useChessContext();

  const imagesObject = Object.fromEntries(
    Object.entries(pieceImages).filter(
      ([key]) =>
        key.startsWith(`${isWhite ? "white" : "black"}`) &&
        !key.includes("pawn") &&
        !key.includes("king")
    )
  );

  // Track window dimensions for dynamic resizing
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const promoteWidth = 400;
  const xPos = Math.round((windowSize.width - promoteWidth) / 2);
  const yPos = Math.round(windowSize.height / 2);

  const handlePromotion = async (promotion_name) => {
    // Promote the pawn in the backend
    await promotePawn(promotion_name);

    setIsPromoting(false)
    initializeData()
  };

  return (
    <div
      style={{ top: `${yPos}px`, left: `${xPos}px` }}
      className="promotionContainer"
    >
      <h3 className="promotionInfo">Choose a promotion:</h3>
      <div>
        {Object.keys(imagesObject).map((image, index) => (
          <div
            key={index}
            className="promotionPiece"
            onClick={() => {
              handlePromotion(image);
            }}
          >
            <img src={imagesObject[image]} alt={image} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default Promote;
