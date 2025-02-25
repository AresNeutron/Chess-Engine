import url from "./url";

const fetchPieces = async () => {
    try {
      const res = await fetch(url + "pieces/");
      if (!res.ok) {
        console.error("Fetch Pieces Function failed");
        return {};
      }

      const response = await res.json();

      return response;
    } catch (err) {
      console.error(err);
      return {};
    }
  };

export default fetchPieces