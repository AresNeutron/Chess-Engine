import url from "./url";

const getMoves = async (piece_name) => {
    try {
      const res = await fetch(url + "valid-moves/" + piece_name);
      if (!res.ok) {
        console.error("Get Moves Function failed");
        return [];
      }

      const response = await res.json();

      return response["valid_moves"];
    } catch (err) {
      console.error(err);
      return [];
    }
  };

export default getMoves