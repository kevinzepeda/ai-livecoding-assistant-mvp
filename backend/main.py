from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from session_store import get_session, store_message
from agent_router import route_message

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}

@app.websocket("/ws/{session_code}")
async def websocket_endpoint(websocket: WebSocket, session_code: str):
    await websocket.accept()
    session = get_session(session_code)
    sessions[session_code] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            response = await route_message(session_code, data)
            store_message(session_code, "user", data)
            store_message(session_code, "assistant", response)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        del sessions[session_code]
