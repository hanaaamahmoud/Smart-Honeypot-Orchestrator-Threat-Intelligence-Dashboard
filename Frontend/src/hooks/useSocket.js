import { useCallback, useEffect, useRef, useState } from "react";

import { createEventsWebSocket, normalizeEvent } from "../services/api";

function fingerprint(event) {
  return [
    event.id,
    event.timestamp,
    event.sourceIp,
    event.sessionId,
    event.protocol,
    event.honeypot,
  ].join("|");
}

function useSocket(enabled = true) {
  const socketRef = useRef(null);
  const reconnectRef = useRef(null);
  const activeRef = useRef(false);
  const connectRef = useRef(null);
  const [isConnected, setIsConnected] = useState(false);
  const [events, setEvents] = useState([]);

  const scheduleReconnect = useCallback(() => {
    if (!activeRef.current || reconnectRef.current !== null) return;
    reconnectRef.current = window.setTimeout(() => {
      reconnectRef.current = null;
      connectRef.current?.();
    }, 5000);
  }, []);

  const connect = useCallback(() => {
    if (!enabled || !activeRef.current) return;

    const current = socketRef.current;
    if (
      current &&
      (current.readyState === WebSocket.OPEN ||
        current.readyState === WebSocket.CONNECTING)
    )
      return;

    let socket;
    try {
      socket = createEventsWebSocket();
    } catch {
      setIsConnected(false);
      scheduleReconnect();
      return;
    }

    socketRef.current = socket;

    socket.onopen = () => {
      if (activeRef.current && socketRef.current === socket)
        setIsConnected(true);
    };

    socket.onmessage = (message) => {
      if (!activeRef.current || socketRef.current !== socket) return;
      try {
        const event = normalizeEvent(JSON.parse(message.data));
        setEvents((currentEvents) => {
          const exists = currentEvents.some(
            (item) => fingerprint(item) === fingerprint(event),
          );
          return exists
            ? currentEvents
            : [event, ...currentEvents].slice(0, 100);
        });
      } catch {
        // Ignore malformed WebSocket messages; HTTP data remains available.
      }
    };

    socket.onclose = () => {
      if (socketRef.current === socket) socketRef.current = null;
      if (!activeRef.current) return;
      setIsConnected(false);
      scheduleReconnect();
    };

    socket.onerror = () => {
      if (activeRef.current) setIsConnected(false);
    };
  }, [enabled, scheduleReconnect]);

  useEffect(() => {
    connectRef.current = connect;
    activeRef.current = enabled;
    const startupTimer = enabled ? window.setTimeout(() => connect(), 0) : null;

    return () => {
      if (startupTimer !== null) window.clearTimeout(startupTimer);
      activeRef.current = false;
      if (reconnectRef.current !== null) {
        window.clearTimeout(reconnectRef.current);
        reconnectRef.current = null;
      }
      const socket = socketRef.current;
      socketRef.current = null;
      if (socket) {
        socket.onclose = null;
        socket.onerror = null;
        socket.onmessage = null;
        socket.onopen = null;
        socket.close();
      }
    };
  }, [connect, enabled]);

  return {
    isConnected,
    events,
    disconnect: () => {
      activeRef.current = false;
      if (reconnectRef.current !== null) {
        window.clearTimeout(reconnectRef.current);
        reconnectRef.current = null;
      }
      const socket = socketRef.current;
      socketRef.current = null;
      if (socket) socket.close();
      setIsConnected(false);
    },
  };
}

export default useSocket;
