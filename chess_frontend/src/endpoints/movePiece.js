import url from "./url";

const movePiece = async (to_pos, piece_name) => {
  try {
    const res = await fetch(url + "move/", {
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify({ "to_pos": to_pos, "piece_name": piece_name }),
    });
    if (!res.ok) {
      console.error("Error in the move function");
    }
  } catch (err) {
    console.error(err);
  }
};

export default movePiece;
