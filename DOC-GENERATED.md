# BMO Data Validation Web Application - Python Files Documentation

## Core Application Files

### **main.py** - FastAPI Backend Server
**Purpose**: Main web server providing REST API endpoints and serving the frontend application.

**Key Features**:
- FastAPI application with CORS middleware
- User authentication with token-based sessions
- REST API endpoints for reports, banks, errors, and comments
- WebSocket support for real-time communication
- Integration with MCP Agent for chatbot functionality
- Static file serving for frontend (client folder)

**Main Endpoints**:
- `/api/login` - User authentication
- `/api/reports` - Report management (GET, PUT status)
- `/api/banks` - Bank CRUD operations
- `/api/errors/{id}/comments` - Error comment management
- `/api/chat` - Chatbot integration

### **database.py** - Database Management
**Purpose**: SQLite database initialization and connection management.

**Key Features**:
- Database schema creation (users, banks, reports, validation_errors, error_comments, sessions)
- Connection factory with Row factory for dict-like access
- Database initialization on startup

**Tables Created**:
- `users` - BMO analyst accounts
- `banks` - Monitored financial institutions
- `reports` - Bank report submissions
- `validation_errors` - Data validation issues
- `error_comments` - Analyst comments on errors
- `sessions` - User authentication tokens

### **models.py** - Pydantic Data Models
**Purpose**: Data validation and serialization models for API requests/responses.

**Models Defined**:
- `LoginRequest`, `User` - Authentication
- `Bank`, `Report` - Core business entities
- `ValidationError`, `ErrorComment` - Error management
- `CommentRequest`, `StatusUpdateRequest` - API request models

## Data Management

### **seed_data.py** - Database Seeding
**Purpose**: Populates database with realistic test data for development and demo.

**Generated Data**:
- 13 test users (analysts, supervisors, admin)
- 20 banks with real ABA codes (JPMorgan Chase, Bank of America, etc.)
- 30 report submissions (Jan-June 2025)
- Validation errors with sample analyst comments

## MCP (Model Context Protocol) Integration

### **mcp_agent.py** - MCP Agent Coordinator
**Purpose**: Orchestrates communication between the chatbot and MCP servers using AWS Bedrock.

**Key Features**:
- AWS Bedrock integration (Claude 3.5 Sonnet model)
- Multi-server MCP client management
- Thread-based conversation tracking
- LangGraph agent with React pattern
- Tool integration from MCP servers

### **bmo_mcp_server.py** - BMO Operations MCP Server
**Purpose**: Exposes BMO business operations as MCP tools for the AI agent.

**Tools Provided**:
- `get_banks()` - Retrieve all banks
- `get_reports()` - Get all reports
- `get_reports_by_status()` - Filter reports by status
- `get_report_errors()` - Get validation errors for reports
- `add_error_comment()` - Add analyst comments
- `update_report_status()` - Accept/reject reports
- `create_bank()`, `update_bank()`, `delete_bank()` - Bank management
- `send_chat_message()` - Internal communication

**Port**: 9008 (SSE transport)

### **sql_mcp_server.py** - SQL Query MCP Server
**Purpose**: Enables AI agent to execute SQL queries against the BMO database.

**Tools Provided**:
- `get_database_schema()` - Returns complete SQLite schema
- `execute_sql_query()` - Executes SQL and returns markdown tables

**Features**:
- SQLite-specific schema introspection
- Markdown table formatting for results
- Security restrictions (SELECT queries only in commented code)

**Port**: 9009 (SSE transport)

### **utils_mcp_server.py** - Utility MCP Server (Unused)
**Purpose**: Generic API calling utilities (appears to be experimental/unused).

**Features**:
- Generic HTTP API calling functions
- URL path parameter replacement
- Environment-based configuration

## Project Architecture

The application follows a **microservices-like architecture** with MCP:

1. **Frontend**: Single-page Vue.js application (client/index.html)
2. **Backend API**: FastAPI server (main.py) 
3. **Database**: SQLite with schema management (database.py)
4. **AI Integration**: MCP Agent (mcp_agent.py) coordinates with:
   - BMO Operations Server (bmo_mcp_server.py)
   - SQL Query Server (sql_mcp_server.py)
5. **Data Models**: Pydantic schemas (models.py)
6. **Test Data**: Seeding utilities (seed_data.py)

The MCP servers run independently and communicate with the main application through the MCP Agent, enabling the AI chatbot to perform complex BMO operations and SQL queries.