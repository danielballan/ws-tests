## Usage

```
❯ pixi run serve
✨ Pixi task (serve): python server.py
INFO:     Started server process [58683]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

```
 pixi run client
✨ Pixi task (client): http ws://localhost:8000/ws
Hello world
> Connected to ws://localhost:8000/ws
> Type a message and press enter to send it.
> The backslash at the end of a line is treated as input not ended.
> Press Ctrl+C to close the connection.
HTTP/1.1 200
connection: Upgrade
date: Tue, 01 Jul 2025 18:03:20 GMT
sec-websocket-accept: hthw56pUAXIytkqZeVtZnYM6TfE=
server: uvicorn
upgrade: websocket

Websocket connection info:
Close Code: 1000
Close Msg:
```

Server logs will show:

```
INFO:     127.0.0.1:56334 - "WebSocket /ws" [accepted]
INFO:     connection open
INFO:     connection closed
```
