import { WebSocketServer } from 'ws';
import { spawn } from 'node-pty';
import os from 'os';
import { parse } from 'url'

const wss = new WebSocketServer({ port: 5000, host:"0.0.0.0" });
// 
wss.on('connection', (ws, req) => {
  const parsedUrl = parse(req.url || '', true)
  const query = parsedUrl.query
  const expected = Buffer.from(`${process.env.ADMIN_PASSWORD}:${process.env.SECRET_KEY}`).toString('base64')
  if(query.token != expected){
    console.log("인증 실패, 연결 종료")
    ws.close();
    return;
  }

  const shell = os.platform() === 'win32' ? 'powershell.exe' : 'bash';
  const ptyProcess = spawn(shell, [], {
    name: 'xterm-color',
    cols: 80,
    rows: 30,
    cwd: process.env.HOME,
    env: process.env,
  });

  ws.on('message', (data) => {
    ptyProcess.write(data.toString());
  });

  ptyProcess.on('data', (data) => {
    ws.send(data);
  });

  ws.on('close', () => {
    ptyProcess.kill();
  });
});

console.log('WebSocket server is running on ws://localhost:5000');