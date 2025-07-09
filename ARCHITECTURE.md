# BMO Data Validation Web Application - Architecture

## Overview

The BMO (Banks Monitoring Office) Data Validation Web Application is a comprehensive system designed for regulatory compliance monitoring of bank reports. The application integrates modern web technologies with AI-powered chat capabilities through the Model Context Protocol (MCP) to provide analysts with intelligent assistance in report validation and decision-making.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                             │
├─────────────────────────────────────────────────────────────────┤
│  Vue.js 3 SPA + Vuetify 3 UI + WebSocket + Chat Interface      │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP/WebSocket
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                            │
├─────────────────────────────────────────────────────────────────┤
│  • REST API Endpoints                                          │
│  • Authentication & Session Management                         │
│  • WebSocket Support                                           │
│  • MCP Agent Integration                                       │
└─────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   SQLite DB     │ │   MCP Server    │ │  AWS Bedrock    │
│                 │ │                 │ │                 │
│ • Users         │ │ • BMO Tools     │ │ • Claude 3.5    │
│ • Banks         │ │ • API Wrapper   │ │   Sonnet        │
│ • Reports       │ │ • SSE Transport │ │ • LangGraph     │
│ • Errors        │ │                 │ │   Agent         │
│ • Comments      │ └─────────────────┘ └─────────────────┘
│ • Sessions      │
└─────────────────┘
```

## Technology Stack

### Frontend
- **Vue.js 3**: Progressive JavaScript framework for building user interfaces
- **Vuetify 3**: Material Design component framework
- **Vue Router 4**: Client-side routing
- **Marked.js**: Markdown parsing for chat responses
- **WebSocket**: Real-time communication support

### Backend
- **FastAPI**: Modern Python web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pydantic**: Data validation using Python type annotations
- **SQLite**: Lightweight database for data persistence

### AI & MCP Integration
- **AWS Bedrock**: Cloud-based AI service platform
- **Claude 3.5 Sonnet**: Large language model for intelligent responses
- **LangGraph**: Framework for building stateful, multi-actor applications with LLMs
- **LangChain MCP Adapters**: Integration layer for Model Context Protocol
- **FastMCP**: Python framework for building MCP servers

### Infrastructure
- **Model Context Protocol (MCP)**: Standardized protocol for AI tool integration
- **Server-Sent Events (SSE)**: Real-time communication between MCP components
- **Token-based Authentication**: Secure session management

## Core Components

### 1. Web Application (`main.py`)
The central FastAPI application that orchestrates all system components:

**Key Features:**
- RESTful API endpoints for CRUD operations
- Token-based authentication system
- WebSocket support for real-time features
- MCP Agent integration for AI capabilities
- Session management with database persistence

**API Endpoints:**
- `/api/login` - User authentication
- `/api/reports` - Report management
- `/api/banks` - Bank registry operations
- `/api/errors/{id}/comments` - Error comment system
- `/api/chat` - AI chat interface

### 2. MCP Server (`bmo_mcp_server.py`)
Specialized MCP server that exposes BMO system capabilities as AI tools:

**Available Tools:**
- `get_banks()` - Retrieve bank registry
- `get_reports()` - Access report submissions
- `get_reports_by_status()` - Filter reports by status
- `get_report_errors()` - Detailed error analysis
- `add_error_comment()` - Analyst comment system
- `update_report_status()` - Accept/reject decisions
- `create_bank()` - Bank registration
- `update_bank()` - Bank information updates
- `delete_bank()` - Bank removal (with constraints)
- `send_chat_message()` - Internal communication

### 3. MCP Agent (`mcp_agent.py`)
AI-powered assistant that provides intelligent support to analysts:

**Capabilities:**
- Natural language query processing
- Context-aware responses using BMO data
- Multi-turn conversation support
- Session-based memory management
- Integration with AWS Bedrock Claude 3.5 Sonnet

**Architecture:**
- LangGraph ReAct agent pattern
- Multi-server MCP client support
- Persistent conversation checkpoints
- Token-based session isolation

### 4. Database Layer (`database.py`)
SQLite-based data persistence with comprehensive schema:

**Tables:**
- `users` - Analyst accounts and roles
- `banks` - Financial institution registry
- `reports` - Regulatory report submissions
- `validation_errors` - Data validation issues
- `error_comments` - Analyst review notes
- `sessions` - Authentication tokens

### 5. Frontend Application (`client/index.html`)
Single-page Vue.js application with comprehensive UI:

**Features:**
- Dashboard with report filtering and search
- Detailed report error analysis
- Comment system for analyst collaboration
- Bank management interface
- Integrated AI chat assistant
- Real-time WebSocket communication

## MCP Integration Architecture

### Protocol Flow
```
Client Request → FastAPI → MCP Agent → MCP Server → BMO Tools → Database
                    ↓
            AI Processing (Bedrock) ← MCP Client ← Tool Results
                    ↓
            Response → Client
```

### MCP Server Configuration
```json
{
  "bmo_mcp_server.py": {
    "url": "http://localhost:9008/sse",
    "transport": "sse"
  }
}
```

### Tool Integration
Each MCP tool provides:
- Comprehensive documentation
- Parameter validation
- Error handling
- Authentication integration
- Audit trail support

## Chat Agent Capabilities

### Natural Language Interface
The AI assistant can:
- Answer questions about reports and banks
- Provide analysis of validation errors
- Assist with decision-making processes
- Generate summaries and insights
- Guide users through workflows

### Context Awareness
- Access to complete BMO database
- Understanding of regulatory requirements
- Knowledge of validation rules
- Awareness of user roles and permissions

### Conversation Management
- Session-based memory using user tokens
- Multi-turn conversation support
- Context preservation across interactions
- Intelligent tool selection and chaining

## Security Architecture

### Authentication
- Token-based session management
- Database-persisted sessions
- Role-based access control
- Secure logout functionality

### Data Protection
- SQL injection prevention through parameterized queries
- Input validation using Pydantic models
- CORS configuration for cross-origin requests
- Session token validation on all protected endpoints

### MCP Security
- Server-side tool execution
- Authenticated API calls
- Session isolation between users
- Audit logging for all operations

## Deployment Architecture

### Development Setup
1. **Database Initialization**: `python seed_data.py`
2. **MCP Server**: `run_mcp_server.bat` (Port 9008)
3. **Web Application**: `run.bat` (Port 8000)

### Production Considerations
- Reverse proxy configuration (Nginx/Apache)
- SSL/TLS termination
- Database migration to PostgreSQL/MySQL
- Container orchestration (Docker/Kubernetes)
- Load balancing for high availability
- Monitoring and logging integration

## Data Flow

### Report Processing Workflow
1. Bank submits report → Database storage
2. Validation engine processes → Error detection
3. Analyst reviews → Comment addition
4. Decision making → Status update
5. Notification → Bank feedback

### AI Assistant Workflow
1. User query → MCP Agent
2. Tool selection → MCP Server
3. Data retrieval → Database
4. AI processing → Bedrock Claude
5. Response generation → User interface

## Scalability Considerations

### Horizontal Scaling
- Stateless FastAPI application design
- Session data in database (not memory)
- MCP server can be distributed
- Load balancer compatible

### Performance Optimization
- Database indexing on frequently queried fields
- Connection pooling for database access
- Caching layer for static data
- Asynchronous processing for AI requests

## Monitoring & Observability

### Logging
- Structured logging throughout application
- Request/response tracking
- Error logging with stack traces
- Performance metrics collection

### Health Checks
- Database connectivity monitoring
- MCP server availability checks
- AI service health validation
- WebSocket connection status

## Future Enhancements

### Planned Features
- Advanced analytics dashboard
- Automated report validation rules
- Integration with external regulatory systems
- Mobile application support
- Advanced AI capabilities (document analysis, trend detection)

### Technical Improvements
- Microservices architecture migration
- Event-driven architecture implementation
- Advanced caching strategies
- Real-time collaboration features
- Enhanced security measures

This architecture provides a robust, scalable foundation for regulatory compliance monitoring while leveraging cutting-edge AI capabilities through the Model Context Protocol integration.