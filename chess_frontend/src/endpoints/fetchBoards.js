import url from "./url";

const fetchBoards = async () => {
    try {
      const res = await fetch(url + "boards/");
      if (!res.ok) {
        console.error("Fetch Boards Function failed");
        return {};
      }

      const response = await res.json();

      return response;
    } catch (err) {
      console.error(err);
      return {};
    }
  };

export default fetchBoards