from fastapi import FastAPI, WebSocket, HTTPException, Depends, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import random
from database import init_database, get_db_connection
from models import LoginRequest, CommentRequest, StatusUpdateRequest
from mcp_agent import MCPAgent

def load_sessions():
    conn = get_db_connection()
    cursor = conn.cursor()
    tokens = cursor.execute("SELECT token FROM sessions").fetchall()
    conn.close()
    return set(row['token'] for row in tokens)

def save_session(token):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO sessions (token) VALUES (?)", (token,))
    conn.commit()
    conn.close()

def remove_session(token):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
    conn.commit()
    conn.close()

# Initialize FastAPI application
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_database()
    
    # Load existing sessions after database is ready
    global active_sessions
    active_sessions = load_sessions()
    await initialize_agent()

    print("BMO Application started successfully")
 
# Create a single instance of MCPAgent
agent = MCPAgent()

# Background task to initialize the agent
async def initialize_agent():
    await agent.initialize()

# # Startup event to initialize the agent
# @app.on_event("startup")
# async def startup_event():
#     await initialize_agent()

@app.on_event("shutdown")
async def shutdown_event():
    await agent.cleanup()



# User session data
user_sessions = {}  # {token: {"user_id": int, "username": str, "websockets": list}}
active_sessions = set()

def check_auth(authorization: str = Header(None)):
    token = authorization.replace("Bearer ", "") if authorization else None
    if not token or token not in active_sessions:
        # Just for testing, allow a default token
        # token = "123456"
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token

@app.post("/api/login")
async def login(credentials: dict):
    print(f"Login attempt for username: {credentials.get('username')}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    user = cursor.execute(
        "SELECT id, username, password, role FROM users WHERE username = ?", 
        (credentials.get('username'),)
    ).fetchone()
    
    if user and user['password'] == credentials.get('password'):
        session_token = str(random.randint(100000000, 999999999))
        active_sessions.add(session_token)
        user_sessions[session_token] = {
            "user_id": user['id'],
            "username": user['username'],
            "role": user['role'],
            "websockets": []
        }
        save_session(session_token)
        conn.close()
        print(f"Login successful for user: {user['username']}")
        return {"token": session_token, "success": True, "user": {"username": user['username'], "role": user['role']}}
    
    conn.close()
    print("Login failed: Invalid credentials")
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/logout")
async def logout(authorization: str = Header(None)):
    token = authorization.replace("Bearer ", "") if authorization else None
    if token and token in active_sessions:
        active_sessions.remove(token)
        if token in user_sessions:
            del user_sessions[token]
        remove_session(token)
    print("User logged out successfully")
    return {"success": True}

@app.get("/api/banks")
async def get_banks(token: str = Depends(check_auth)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    banks = cursor.execute("""
        SELECT id, aba_code, name
        FROM banks
        ORDER BY name
    """).fetchall()
    
    result = [dict(bank) for bank in banks]
    conn.close()
    return result

@app.get("/api/reports")
async def get_reports(token: str = Depends(check_auth)):
    print("Fetching reports list")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    reports = cursor.execute("""
        SELECT r.id, r.report_code, r.submission_date, r.has_errors, r.is_accepted,
               b.aba_code, b.name as bank_name
        FROM reports r
        JOIN banks b ON r.bank_id = b.id
        ORDER BY r.submission_date DESC
    """).fetchall()
    
    result = [dict(report) for report in reports]
    conn.close()
    print(f"Retrieved {len(result)} reports")
    return result

@app.get("/api/reports/status/{status}")
async def get_reports_by_status(status: str, token: str = Depends(check_auth)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if status == "accepted":
        where_clause = "r.is_accepted = 1"
    elif status == "rejected":
        where_clause = "r.is_accepted = 0 AND r.has_errors = 1"
    elif status == "pending":
        where_clause = "r.is_accepted IS NULL"
    else:
        raise HTTPException(status_code=400, detail="Invalid status. Use: accepted, rejected, or pending")
    
    reports = cursor.execute(f"""
        SELECT r.id, r.report_code, r.submission_date, r.has_errors, r.is_accepted,
               b.aba_code, b.name as bank_name
        FROM reports r
        JOIN banks b ON r.bank_id = b.id
        WHERE {where_clause}
        ORDER BY r.submission_date DESC
    """).fetchall()
    
    result = [dict(report) for report in reports]
    conn.close()
    return result

@app.get("/api/reports/{report_id}/errors")
async def get_report_errors(report_id: int, token: str = Depends(check_auth)):
    print(f"Fetching errors for report {report_id}")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    errors = cursor.execute("""
        SELECT ve.id, ve.error_type, ve.error_message, ve.field_name,
               GROUP_CONCAT(u.username || ': ' || ec.comment || ' (' || ec.created_at || ')', '\n') as comments
        FROM validation_errors ve
        LEFT JOIN error_comments ec ON ve.id = ec.error_id
        LEFT JOIN users u ON ec.user_id = u.id
        WHERE ve.report_id = ?
        GROUP BY ve.id
        ORDER BY ve.id
    """, (report_id,)).fetchall()
    
    result = []
    for error in errors:
        error_dict = dict(error)
        error_dict['comments'] = error_dict['comments'].split('\n') if error_dict['comments'] else []
        result.append(error_dict)
    
    conn.close()
    print(f"Retrieved {len(result)} errors for report {report_id}")
    return result

@app.post("/api/errors/{error_id}/comments")
async def add_error_comment(error_id: int, comment_data: CommentRequest, token: str = Depends(check_auth)):
    print(f"Adding comment to error {error_id}")
    
    if token not in user_sessions:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    user_id = user_sessions[token]['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO error_comments (error_id, user_id, comment) VALUES (?, ?, ?)",
        (error_id, user_id, comment_data.comment)
    )
    
    conn.commit()
    conn.close()
    print(f"Comment added successfully to error {error_id}")
    return {"success": True}

@app.put("/api/reports/{report_id}/status")
async def update_report_status(report_id: int, status_data: StatusUpdateRequest, token: str = Depends(check_auth)):
    print(f"Updating report {report_id} status to {'accepted' if status_data.is_accepted else 'rejected'}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE reports SET is_accepted = ? WHERE id = ?",
        (status_data.is_accepted, report_id)
    )
    
    conn.commit()
    conn.close()
    print(f"Report {report_id} status updated successfully")
    return {"success": True}

@app.post("/api/banks")
async def create_bank(bank_data: dict, token: str = Depends(check_auth)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO banks (aba_code, name) VALUES (?, ?)",
        (bank_data['aba_code'], bank_data['name'])
    )
    
    conn.commit()
    conn.close()
    return {"success": True}

@app.put("/api/banks/{bank_id}")
async def update_bank(bank_id: int, bank_data: dict, token: str = Depends(check_auth)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE banks SET aba_code = ?, name = ? WHERE id = ?",
        (bank_data['aba_code'], bank_data['name'], bank_id)
    )
    
    conn.commit()
    conn.close()
    return {"success": True}

@app.delete("/api/banks/{bank_id}")
async def delete_bank(bank_id: int, token: str = Depends(check_auth)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if bank has any reports
    report_count = cursor.execute(
        "SELECT COUNT(*) as count FROM reports WHERE bank_id = ?", 
        (bank_id,)
    ).fetchone()['count']
    
    if report_count > 0:
        conn.close()
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete bank. It has {report_count} associated report(s)."
        )
    
    cursor.execute("DELETE FROM banks WHERE id = ?", (bank_id,))
    
    conn.commit()
    conn.close()
    return {"success": True}

@app.post("/api/chat")
async def chat(message_data: dict, token: str = Depends(check_auth)):
    message = message_data.get('message', '')
    print(f"Received chat message: {message}")
    # response = f"Echo: {message}"
    response = await agent.question(message, token)
    return {"response": response}

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
    print(f"WebSocket connected for user {user_sessions[token]['username']}. Total connections: {len(user_sessions[token]['websockets'])}")
    
    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        print(f"WebSocket error: {e}")
        if token in user_sessions and websocket in user_sessions[token]["websockets"]:
            user_sessions[token]["websockets"].remove(websocket)
            print(f"WebSocket disconnected for user {user_sessions[token]['username']}. Remaining connections: {len(user_sessions[token]['websockets'])}")

# Mount static files
app.mount("/", StaticFiles(directory="client", html=True), name="static")