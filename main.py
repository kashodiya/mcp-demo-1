from fastapi import FastAPI, WebSocket, HTTPException, Depends, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import json
import os
import random

SESSIONS_FILE = "active_sessions.json"
 
def load_sessions():
    try:
        with open(SESSIONS_FILE, 'r') as f:
            print(f"Loading active sessions from {SESSIONS_FILE}")
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_sessions():
    global active_sessions
    with open(SESSIONS_FILE, 'w') as f:
        json.dump(list(active_sessions), f)

# Initialize FastAPI application
app = FastAPI()
 
# User session data
user_sessions = {}  # {token: {"agent_session_id": str, "form_data": dict, "websockets": list}}
active_sessions = load_sessions()

def check_auth(authorization: str = Header(None)):
    token = authorization.replace("Bearer ", "") if authorization else None
    if not token or token not in active_sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token

@app.post("/api/login")
async def login(credentials: dict):
    password = os.getenv("PASS", "123456")
    if credentials.get("password") == password:
        session_token = str(random.randint(100000000, 999999999))
        active_sessions.add(session_token)
        user_sessions[session_token] = {
            "agent_session_id": str(random.randint(10000000, 99999999)),
            "form_data": {},
            "websockets": []
        }
        save_sessions()
        return {"token": session_token, "success": True}
    raise HTTPException(status_code=401, detail="Invalid password")

@app.post("/api/logout")
async def logout(authorization: str = Header(None)):
    token = authorization.replace("Bearer ", "") if authorization else None
    if token and token in active_sessions:
        active_sessions.remove(token)
        if token in user_sessions:
            del user_sessions[token]
        save_sessions()
    return {"success": True}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection accepted")
    
    # Get token from first message
    try:
        message = await websocket.receive_text()
        auth_data = json.loads(message)
        token = auth_data.get("token")
        print(f"Received token: {token}")
    except Exception as e:
        print(f"Failed to get token: {e}")
        await websocket.close()
        return
    
    if not token or token not in active_sessions:
        print(f"Invalid token or session: {token}")
        await websocket.close()
        return
    
    if token not in user_sessions:
        print(f"Token not in user_sessions: {token}")
        await websocket.close()
        return
    
    user_sessions[token]["websockets"].append(websocket)
    print(f"WebSocket connected for token {token}. Total connections: {len(user_sessions[token]['websockets'])}")
    
    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        print(f"WebSocket error: {e}")
        if token in user_sessions and websocket in user_sessions[token]["websockets"]:
            user_sessions[token]["websockets"].remove(websocket)
            print(f"WebSocket disconnected for token {token}. Remaining connections: {len(user_sessions[token]['websockets'])}")

# Mount static files
# app.mount("/", StaticFiles(directory="client/dist", html=True), name="static")
app.mount("/", StaticFiles(directory="client", html=True), name="static")