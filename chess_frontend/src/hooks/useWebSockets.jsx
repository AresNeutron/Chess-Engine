import { useEffect, useRef } from "react";
import url from "../endpoints/url";  // Asegúrate de que esta URL es correcta

const useWebSocket = (onEvent) => {
  const socketRef = useRef(null);  // This is creating a variable to store the web socket after re-renders

  useEffect(() => {
    // Crear conexión WebSocket
    socketRef.current = new WebSocket(`${url.replace("http", "ws")}ws`);

    socketRef.current.onopen = () => {
      console.log("Conectado al WebSocket");
    };

    socketRef.current.onmessage = (event) => {
      const { event: eventType, data } = JSON.parse(event.data);
      console.log(`Evento recibido: ${eventType}`, data);
      onEvent(eventType, data);
    };

    socketRef.current.onclose = () => {
      console.log("Conexión WebSocket cerrada");
    };

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
        socketRef.current = null;
      }
    };
  }, []);

  return socketRef.current;
};

export default useWebSocket;
