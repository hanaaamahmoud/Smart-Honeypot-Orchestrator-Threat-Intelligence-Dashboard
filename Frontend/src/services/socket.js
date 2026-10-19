// const SOCKET_URL = "ws://localhost:8000/ws";

// export function createSocket() {
//   const socket = new WebSocket(SOCKET_URL);

//   return socket;
// }


const SOCKET_URL =
  `${window.location.protocol === "https:" ? "wss:" : "ws:"}//` +
  `${window.location.host}/backend/ws`;

export function createSocket() {
  const socket = new WebSocket(SOCKET_URL);

  return socket;
}