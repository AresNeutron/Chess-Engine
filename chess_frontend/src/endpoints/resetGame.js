import url from "./url";

const resetGame = async () => {
    try {
      await fetch(url + "reset/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
      console.log("Game reset successfully!");
    } catch (error) {
      console.error("Error resetting game:", error);
    }
  };

export default resetGame
  