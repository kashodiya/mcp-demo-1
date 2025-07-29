# BMO Data Validation Web Application

A web application for Banks Monitoring Office (BMO) to validate data submitted by banks.

## Features

- **User Authentication**: Login system for BMO analysts
- **Reports Dashboard**: View all bank reports with status indicators
- **Error Management**: View validation errors for each report
- **Comment System**: Add comments to validation errors
- **Report Approval**: Accept or reject bank reports

## Quick Start

1. **Install Dependencies**:
   ```bash
   uv sync
   ```

2. **Initialize Database** (already done):
   ```bash
   python seed_data.py
   ```

3. **Start Server**:
   - Run MCP servers
   ```cmd
   run_mcp_server.bat
   ```
   - Run web app
   ```cmd
   run.bat
   ```

4. **Access Application**:
   Open http://localhost:8000 in your browser

## Test Users

- **Username**: `analyst1`, **Password**: `123456`
- **Username**: `analyst2`, **Password**: `123456`
- **Username**: `supervisor`, **Password**: `123456`
- **Username**: `admin`, **Password**: `123456`
- **Username**: `reviewer`, **Password**: `123456`

## Database

The application uses SQLite database (`bmo_data.db`) with:
- 5 test users
- 20 banks with realistic ABA codes
- 30 report submissions (Jan-June 2025)
- Validation errors with sample comments

## Technology Stack

- **Frontend**: Vue.js 3 + Vuetify 3 (Single HTML file)
- **Backend**: FastAPI + Python
- **Database**: SQLite
- **Authentication**: Token-based sessions

## API Endpoints

- `POST /api/login` - User authentication
- `GET /api/reports` - List all reports
- `GET /api/reports/{id}/errors` - Get report errors
- `POST /api/errors/{id}/comments` - Add error comment
- `PUT /api/reports/{id}/status` - Accept/reject report