import { useEffect } from "react";
import { io } from "socket.io-client";
import url from "../endpoints/url";

const socket = io(url, { path: "/ws" });

const useWebSocket = (onEvent) => {
  useEffect(() => {
    socket.on("promotion_required", (data) => {
      console.log("Promoción requerida:", data);
      onEvent("promotion_required", data);
    });

    socket.on("check_alert", (data) => {
      console.log("¡Jaque!", data);
      onEvent("check_alert", data);
    });

    socket.on("checkmate_alert", (data) => {
      console.log("¡Jaque mate!", data);
      onEvent("checkmate_alert", data);
    });

    return () => {
      socket.off("promotion_required");
      socket.off("check_alert");
      socket.off("checkmate_alert");
    };
  }, [onEvent]);
};

export default useWebSocket;
