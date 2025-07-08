# Implementation Plan - BMO Data Validation Web Application

## Overview
Building a web application for Banks Monitoring Office (BMO) to validate data submitted by banks, with login/home screens already developed.

## Database Schema & Models

### 1. Database Setup
- **File**: `database.py`
- Create SQLite database with tables:
  - `users` (id, username, password, role)
  - `banks` (id, aba_code, name)
  - `reports` (id, bank_id, report_code, submission_date, has_errors, is_accepted)
  - `validation_errors` (id, report_id, error_type, error_message, field_name)
  - `error_comments` (id, error_id, user_id, comment, created_at)

### 2. Backend API Development

#### Core API Endpoints (`main.py`)
- `POST /api/login` - User authentication
- `GET /api/reports` - List all reports with bank info
- `GET /api/reports/{report_id}/errors` - Get validation errors for a report
- `POST /api/errors/{error_id}/comments` - Add comment to an error
- `PUT /api/reports/{report_id}/status` - Accept/reject report

#### Data Models (`models.py`)
- Pydantic models for request/response validation
- User, Bank, Report, ValidationError, ErrorComment classes

### 3. Frontend Components

#### Reports List View
- Table showing: Bank ABA, Report Code, Submission Date, Error Status, Acceptance Status
- Filter/search functionality
- Action buttons for each report

#### Report Details Modal
- Display validation errors for selected report
- Show existing comments
- Add new comments interface
- Accept/Reject report buttons

#### Error Management
- Error details display
- Comment history
- Add comment form

### 4. Seed Data Creation

#### Data Generation Script (`seed_data.py`)
- 5 BMO analyst users
- 20 banks with realistic ABA codes
- 30 report submissions (Jan-June 2025)
- 50+ validation errors across reports
- Sample comments on various errors

## Implementation Steps

### Phase 1: Backend Foundation
1. Set up FastAPI project structure
2. Create database schema and models
3. Implement authentication endpoints
4. Create seed data script

### Phase 2: Core API Development
1. Reports listing endpoint
2. Report errors retrieval
3. Comment management endpoints
4. Report status update endpoints

### Phase 3: Frontend Integration
1. Update existing login to use backend API
2. Enhance home screen with reports table
3. Add report details modal
4. Implement error commenting system
5. Add accept/reject functionality

### Phase 4: Testing & Polish
1. Add console logging throughout
2. Test all user workflows
3. Verify seed data integration
4. Final UI/UX adjustments

## File Structure
```
mcp-demo-1/
├── backend/
│   ├── main.py           # FastAPI app
│   ├── database.py       # Database setup
│   ├── models.py         # Pydantic models
│   └── seed_data.py      # Data generation
├── index.html            # Single-page frontend
├── requirements.txt      # Python dependencies
└── bmo_data.db          # SQLite database
```

## Key Features to Implement
- ✅ Login system (existing)
- ✅ Home screen (existing)
- 🔄 Reports listing with status indicators
- 🔄 Error details view and management
- 🔄 Comment system for errors
- 🔄 Report acceptance/rejection workflow
- 🔄 Seed data with realistic scenarios

## Technical Considerations
- Single HTML file with Vue.js components
- SQLite for simple data persistence
- Clear text passwords (demo only)
- Extensive console logging for debugging
- Responsive design with Vuetify components