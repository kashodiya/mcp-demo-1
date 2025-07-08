from typing import Dict, Any, List, Optional
import requests
import sqlite3
from fastmcp import FastMCP

mcp = FastMCP("BMO MCP Server")
BASE_URL = "http://localhost:8000"

def get_latest_token() -> Optional[str]:
    """Get the most recent token from sessions table."""
    try:
        conn = sqlite3.connect('bmo_data.db')
        cursor = conn.cursor()
        result = cursor.execute("SELECT token FROM sessions ORDER BY rowid DESC LIMIT 1").fetchone()
        conn.close()
        return result[0] if result else None
    except Exception:
        return None

# @mcp.tool()
# def login_user(username: str, password: str) -> Dict[str, Any]:
#     """Authenticate user and get access token."""
#     try:
#         response = requests.post(f"{BASE_URL}/api/login", json={"username": username, "password": password})
#         return response.json()
#     except Exception as e:
#         return {"error": str(e)}

@mcp.tool()
def get_banks() -> List[Dict[str, Any]]:
    """Get list of all banks with their ABA codes and names. If you want to search any bank by name, first get all banks and find matching name in the list."""
    token = get_latest_token()
    if not token:
        return {"error": "No active session found"}
    try:
        response = requests.get(f"{BASE_URL}/api/banks", headers={"Authorization": f"Bearer {token}"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_reports() -> List[Dict[str, Any]]:
    """Get list of all bank reports."""
    token = get_latest_token()
    if not token:
        return {"error": "No active session found"}
    try:
        response = requests.get(f"{BASE_URL}/api/reports", headers={"Authorization": f"Bearer {token}"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_report_errors(report_id: int) -> List[Dict[str, Any]]:
    """Get validation errors for a specific report."""
    token = get_latest_token()
    if not token:
        return {"error": "No active session found"}
    try:
        response = requests.get(f"{BASE_URL}/api/reports/{report_id}/errors", headers={"Authorization": f"Bearer {token}"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def add_error_comment(error_id: int, comment: str) -> Dict[str, Any]:
    """Add a comment to a validation error."""
    token = get_latest_token()
    if not token:
        return {"error": "No active session found"}
    try:
        response = requests.post(f"{BASE_URL}/api/errors/{error_id}/comments", json={"comment": comment}, headers={"Authorization": f"Bearer {token}"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def update_report_status(report_id: int, is_accepted: bool) -> Dict[str, Any]:
    """Accept or reject a bank report."""
    token = get_latest_token()
    if not token:
        return {"error": "No active session found"}
    try:
        response = requests.put(f"{BASE_URL}/api/reports/{report_id}/status", json={"is_accepted": is_accepted}, headers={"Authorization": f"Bearer {token}"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def send_chat_message(message: str) -> Dict[str, Any]:
    """Send a message to the chat system."""
    token = get_latest_token()
    if not token:
        return {"error": "No active session found"}
    try:
        response = requests.post(f"{BASE_URL}/api/chat", json={"message": message}, headers={"Authorization": f"Bearer {token}"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="sse", port=9008)
    
