from typing import Dict, Any, List
import sqlite3
from fastmcp import FastMCP

mcp = FastMCP("BMO SQL MCP Server")
DATABASE_PATH = "bmo_data.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@mcp.tool()
def get_database_schema() -> Dict[str, Any]:
    """Get complete database schema for BMO SQLite database.
    
    Database System: SQLite 3.x
    SQL Dialect: SQLite SQL (standard SQL with SQLite extensions)
    
    Returns schema with tables, columns, types, constraints, and relationships.
    Use this before generating SQL queries to ensure accuracy.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        schema = {
            "database_type": "SQLite",
            "sql_dialect": "SQLite SQL",
            "tables": {}
        }
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            cursor.execute(f"PRAGMA foreign_key_list({table_name})")
            foreign_keys = cursor.fetchall()
            
            schema["tables"][table_name] = {
                "columns": [{"name": col[1], "type": col[2], "not_null": bool(col[3]), "primary_key": bool(col[5])} for col in columns],
                "foreign_keys": [{"column": fk[3], "references_table": fk[2], "references_column": fk[4]} for fk in foreign_keys]
            }
        
        conn.close()
        return schema
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def execute_sql_query(sql_query: str) -> Dict[str, Any]:
    """Execute SQL queries against BMO SQLite database.
    
    Supports SELECT, INSERT, UPDATE, DELETE operations.
    Returns structured results suitable for analysis and markdown table formatting.
    
    For tabular data, format results as markdown tables for better readability.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        query_type = sql_query.strip().upper().split()[0]
        
        if query_type == "SELECT":
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            data = [dict(row) for row in results]
            
            response = {
                "success": True,
                "data": data,
                "columns": columns,
                "row_count": len(data)
            }
        else:
            conn.commit()
            response = {
                "success": True,
                "affected_rows": cursor.rowcount
            }
        
        conn.close()
        return response
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def format_as_markdown_table(query_results: Dict[str, Any]) -> str:
    """Convert SQL query results to markdown table format for display.
    
    Takes results from execute_sql_query and formats as readable markdown table.
    """
    try:
        if not query_results.get("success"):
            return f"Error: {query_results.get('error', 'Query failed')}"
        
        data = query_results.get("data", [])
        columns = query_results.get("columns", [])
        
        if not data or not columns:
            return "No data to display."
        
        header = "| " + " | ".join(columns) + " |"
        separator = "| " + " | ".join(["---"] * len(columns)) + " |"
        
        rows = []
        for row in data:
            values = [str(row.get(col, "NULL")) for col in columns]
            rows.append("| " + " | ".join(values) + " |")
        
        return "\n".join([header, separator] + rows) + f"\n\n*{len(data)} row(s) returned*"
    except Exception as e:
        return f"Error formatting table: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="sse", port=9009)