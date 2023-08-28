from fastapi import WebSocket, WebSocketDisconnect, APIRouter

web_socket_rout = APIRouter()

websocket_connections = []


async def send_notification(message: str):
    for connection in websocket_connections:
        await connection.send_text(message)


@web_socket_rout.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()

    except WebSocketDisconnect:
        websocket_connections.remove(websocket)
