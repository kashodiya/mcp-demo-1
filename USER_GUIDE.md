# BMO Data Validation Web Application - User Guide

## Overview

The Banks Monitoring Office (BMO) Data Validation Web Application is a comprehensive tool designed for BMO analysts to review, validate, and manage data submissions from banks. This application helps ensure data quality and compliance for economic policy making and bank governance.

## Getting Started

### System Requirements
- Web browser (Chrome, Firefox, Safari, Edge)
- Internet connection
- Access credentials provided by system administrator

### Accessing the Application
1. Open your web browser
2. Navigate to: `http://localhost:8000`
3. You will be redirected to the login page

## User Authentication

### Login Process
1. Enter your **Username** and **Password**
2. Click **Login** button
3. Upon successful authentication, you'll be redirected to the Reports Dashboard

### Test User Accounts
For demonstration purposes, the following test accounts are available:

| Username   | Password | Role        |
|------------|----------|-------------|
| analyst1   | 123456   | Analyst     |
| analyst2   | 123456   | Analyst     |
| supervisor | 123456   | Supervisor  |
| admin      | 123456   | Administrator |
| reviewer   | 123456   | Reviewer    |

### Logout
- Click the **Logout** button in the top navigation bar to end your session

## Reports Dashboard

### Overview
The main dashboard displays all bank report submissions in a comprehensive table format.

### Report Information
Each report entry shows:
- **Bank Name**: Name of the submitting bank
- **ABA Code**: American Bankers Association routing number
- **Report Code**: Unique identifier for the report type
- **Submission Date**: When the report was submitted
- **Error Status**: Visual indicator showing if validation errors exist
- **Approval Status**: Current approval state (Pending/Accepted/Rejected)

### Status Indicators
- **🔴 Red Circle**: Report contains validation errors
- **🟢 Green Circle**: Report passed validation
- **📋 Pending**: Awaiting review and approval
- **✅ Accepted**: Report approved and processed
- **❌ Rejected**: Report rejected due to issues

## Error Management

### Viewing Validation Errors
1. Locate the report with error indicators in the dashboard
2. Click **View Errors** button for that report
3. A detailed error list will display showing:
   - Error type/category
   - Specific error description
   - Field or section affected
   - Severity level

### Error Details
Each validation error includes:
- **Error ID**: Unique identifier
- **Error Type**: Category of validation failure
- **Description**: Detailed explanation of the issue
- **Field Reference**: Specific data field with the error
- **Comments**: Analyst notes and observations

## Comment System

### Adding Comments to Errors
1. Navigate to the error details view
2. Locate the specific error requiring commentary
3. Click **Add Comment** button
4. Enter your comment in the text field
5. Click **Save Comment** to record your observation

### Comment Guidelines
- Be specific and actionable
- Reference relevant regulations or standards
- Provide clear guidance for correction
- Use professional language
- Include your analyst ID for tracking

### Viewing Existing Comments
- Comments appear chronologically below each error
- Each comment shows:
  - Comment text
  - Author information
  - Timestamp
  - Comment ID

## Report Approval Process

### Approval Options
For each report, you can:
- **Accept**: Approve the report for processing
- **Reject**: Decline the report due to issues
- **Leave Pending**: Keep under review

### Accepting Reports
1. Review all validation errors (if any)
2. Ensure all issues are resolved or acceptable
3. Click **Accept Report** button
4. Confirm your decision in the dialog box
5. Report status updates to "Accepted"

### Rejecting Reports
1. Identify critical issues or unresolved errors
2. Add comments explaining rejection reasons
3. Click **Reject Report** button
4. Provide rejection justification
5. Report status updates to "Rejected"

### Approval Workflow
1. **Initial Submission**: Report enters "Pending" status
2. **Analyst Review**: Validation errors identified and commented
3. **Decision Making**: Accept or reject based on error severity
4. **Final Status**: Report marked as Accepted or Rejected

## Navigation and Interface

### Main Navigation
- **Dashboard**: Return to reports overview
- **Reports**: Access all report submissions
- **Profile**: User account information
- **Logout**: End current session

### Search and Filtering
- Use search functionality to find specific banks or reports
- Filter by date range, status, or error presence
- Sort columns by clicking headers

### Responsive Design
- Application adapts to different screen sizes
- Mobile-friendly interface for tablet access
- Consistent experience across devices

## Data Management

### Report Data Structure
Reports contain various financial and regulatory data including:
- Balance sheet information
- Income statements
- Regulatory compliance metrics
- Customer data
- Transaction volumes

### Validation Rules
The system automatically validates:
- Data format compliance
- Numerical accuracy
- Required field completion
- Regulatory threshold adherence
- Cross-field consistency

### Error Categories
Common validation errors include:
- **Format Errors**: Incorrect data types or formats
- **Missing Data**: Required fields left blank
- **Calculation Errors**: Mathematical inconsistencies
- **Regulatory Violations**: Non-compliance with banking regulations
- **Data Inconsistencies**: Conflicting information across fields

## Best Practices

### Daily Workflow
1. Login and review new report submissions
2. Prioritize reports with validation errors
3. Systematically review each error
4. Add meaningful comments for guidance
5. Make approval decisions based on error severity
6. Document any unusual findings

### Quality Assurance
- Double-check critical calculations
- Verify regulatory compliance
- Cross-reference with previous submissions
- Escalate complex issues to supervisors
- Maintain detailed audit trails

### Communication
- Use clear, professional language in comments
- Provide specific guidance for error correction
- Reference relevant regulations when applicable
- Coordinate with team members on complex cases

## Troubleshooting

### Common Issues
- **Login Problems**: Verify credentials and contact administrator
- **Slow Loading**: Check internet connection and refresh browser
- **Missing Data**: Ensure proper permissions and data availability
- **Error Display Issues**: Clear browser cache and reload

### Technical Support
- Contact system administrator for technical issues
- Report bugs or system errors promptly
- Keep browser updated for optimal performance
- Use supported browsers for best experience

## Security and Compliance

### Data Protection
- All data transmissions are secured
- User sessions automatically timeout
- Access logs maintained for audit purposes
- Sensitive information protected

### Audit Trail
- All user actions are logged
- Comment history preserved
- Approval decisions tracked
- System maintains complete audit trail

## System Information

### Technology Stack
- **Frontend**: Vue.js 3 with Vuetify 3 components
- **Backend**: FastAPI Python framework
- **Database**: SQLite for data storage
- **Authentication**: Token-based session management

### Database Contents
- 5 user accounts with different roles
- 20 banks with realistic ABA codes
- 30 report submissions (January-June 2025)
- Validation errors with sample comments

## Support and Contact

For technical support, training, or system issues:
- Contact your system administrator
- Reference this user guide for standard procedures
- Report bugs or enhancement requests through proper channels
- Participate in training sessions for system updates

---

*This user guide covers the core functionality of the BMO Data Validation Web Application. For additional features or advanced operations, consult with your system administrator or refer to technical documentation.*