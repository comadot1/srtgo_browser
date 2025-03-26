import { WebSocketServer } from "ws";
import pty from "node-pty"; 

const wss = new WebSocketServer({ port: 8099 });

wss.on("connection", (ws, req) => {
  console.log(`Client connected from: ${req.socket.remoteAddress}`);

  const shell = pty.spawn("bash", [], {
    name: "xterm-color",
    cols: 80,
    rows: 24,
    cwd: process.env.HOME,
    env: process.env,
  });

  shell.on("data", (data) => ws.send(data));

  ws.on("message", (message) => {
    shell.write(message.toString());
  });

  ws.on("close", () => {
    console.log("Client disconnected");
    shell.kill();
  });

  ws.on("error", (err) => {
    console.error("WebSocket error:", err);
  });
});

console.log("WebSocket server running on ws://192.168.219.58:8099");
