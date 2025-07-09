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
    """Retrieve a comprehensive list of all banks registered in the BMO system.
    
    This tool provides access to the complete bank registry maintained by the Banks Monitoring Office.
    Each bank entry includes essential identification information needed for report processing and validation.
    
    Returns:
    List of bank objects, each containing:
    - id: Unique internal bank identifier used for system operations
    - aba_code: 9-digit American Bankers Association routing number (e.g., "021000021")
    - name: Full legal name of the financial institution
    
    Use cases:
    - Searching for banks by name (retrieve full list then filter by name)
    - Validating bank existence before processing reports
    - Getting bank IDs for update/delete operations
    - Displaying bank selection lists in user interfaces
    - Cross-referencing ABA codes with bank names
    
    Search workflow:
    1. Call this function to get all banks
    2. Filter results by name, ABA code, or other criteria
    3. Use the bank ID for subsequent operations
    
    Note: This returns all active banks in the system. For specific bank searches,
    retrieve the full list and apply client-side filtering.
    """
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
    """Retrieve all bank reports submitted to the BMO system for validation and review.
    
    This tool provides access to the complete repository of regulatory reports submitted by
    monitored banks. Reports include submission metadata, validation status, and approval information.
    
    Returns:
    List of report objects, each containing:
    - id: Unique report identifier for system operations
    - report_code: Bank-generated report reference code
    - submission_date: When the report was submitted (ISO format)
    - has_errors: Boolean indicating if validation errors were found
    - is_accepted: Approval status (true=accepted, false=rejected, null=pending)
    - aba_code: ABA routing number of the submitting bank
    - bank_name: Full name of the submitting bank
    
    Use cases:
    - Dashboard overview of all report submissions
    - Monitoring report processing pipeline status
    - Identifying reports requiring analyst attention
    - Generating compliance and processing statistics
    - Finding specific reports for detailed review
    
    Report status interpretation:
    - has_errors=false, is_accepted=true: Clean, approved reports
    - has_errors=true, is_accepted=false: Reports with validation issues, rejected
    - has_errors=true/false, is_accepted=null: Reports awaiting analyst review
    
    For filtered views, use get_reports_by_status() instead.
    """
    token = get_latest_token()
    if not token:
        return {"error": "No active session found"}
    try:
        response = requests.get(f"{BASE_URL}/api/reports", headers={"Authorization": f"Bearer {token}"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_reports_by_status(status: str) -> List[Dict[str, Any]]:
    """Get bank reports filtered by status. 
    
    Parameters:
    - status: Report status to filter by. Valid values are:
        - 'accepted': Reports that have been approved
        - 'rejected': Reports that have been rejected (have errors and is_accepted=false)
        - 'pending': Reports that are awaiting review (is_accepted=null)
    
    Returns list of reports with bank information including id, report_code, submission_date, has_errors, is_accepted, aba_code, and bank_name.
    """
    token = get_latest_token()
    if not token:
        return {"error": "No active session found"}
    try:
        response = requests.get(f"{BASE_URL}/api/reports/status/{status}", headers={"Authorization": f"Bearer {token}"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_report_errors(report_id: int) -> List[Dict[str, Any]]:
    """Retrieve detailed validation errors for a specific bank report.
    
    This tool provides comprehensive error information for reports that failed BMO validation
    rules. Each error includes technical details and analyst comments to support the review process.
    
    Parameters:
    - report_id: Unique identifier of the report to examine. Use get_reports() to find report IDs.
    
    Returns:
    List of error objects, each containing:
    - id: Unique error identifier for comment operations
    - error_type: Category of validation failure (e.g., "Data Format", "Missing Field")
    - description: Detailed explanation of the validation issue
    - field_name: Specific data field that caused the error (if applicable)
    - comments: List of analyst comments and notes about this error
    
    Use cases:
    - Detailed error analysis for report rejection decisions
    - Providing feedback to banks on submission issues
    - Tracking common validation problems across institutions
    - Supporting analyst review and decision-making process
    - Generating error reports and compliance statistics
    
    Error types commonly found:
    - "Data Format": Incorrect data formatting or structure
    - "Missing Field": Required information not provided
    - "Invalid Value": Data values outside acceptable ranges
    - "Business Rule": Violations of regulatory business logic
    
    Workflow:
    1. Use get_reports() to find reports with has_errors=true
    2. Call this function with the report_id to get error details
    3. Use add_error_comment() to add analyst notes
    4. Use update_report_status() to accept/reject after review
    """
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
    """Add analyst comments and notes to specific validation errors.
    
    This tool enables BMO analysts to document their review process, provide feedback
    to banks, and maintain an audit trail of error resolution activities.
    
    Parameters:
    - error_id: Unique identifier of the validation error. Use get_report_errors() to find error IDs.
    - comment: Analyst comment or note about the error. Should be professional and informative.
    
    Returns:
    - success: True if comment was added successfully
    - error: Error message if operation failed
    
    Use cases:
    - Documenting analyst review findings and decisions
    - Providing specific feedback to banks on data issues
    - Recording resolution steps or recommendations
    - Maintaining compliance audit trails
    - Communicating between analysts on complex errors
    
    Comment best practices:
    - Be specific about the issue and required corrections
    - Reference relevant regulatory requirements when applicable
    - Provide clear guidance for bank remediation
    - Use professional, constructive language
    - Include analyst initials or identification when needed
    
    Example comments:
    - "Field requires YYYY-MM-DD format, received MM/DD/YYYY"
    - "Amount exceeds regulatory threshold, requires additional documentation"
    - "Missing required signature on page 3 of attachment"
    - "Reviewed with supervisor - acceptable under exception criteria"
    
    Workflow:
    1. Use get_report_errors() to identify errors needing comments
    2. Add detailed, actionable comments for each error
    3. Comments become part of the permanent audit record
    4. Banks can view comments to understand required corrections
    """
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
    """Make final acceptance or rejection decisions on bank reports after validation review.
    
    This tool represents the culmination of the BMO review process, where analysts make
    official determinations on report compliance. This action triggers notifications to
    banks and updates regulatory compliance records.
    
    Parameters:
    - report_id: Unique identifier of the report to approve/reject. Use get_reports() to find report IDs.
    - is_accepted: Final decision (true=accept report, false=reject report)
    
    Returns:
    - success: True if status was updated successfully
    - error: Error message if operation failed
    
    Decision criteria:
    - Accept (true): Report meets all regulatory requirements and validation rules
    - Reject (false): Report has errors that prevent regulatory acceptance
    
    Use cases:
    - Finalizing report review after error analysis
    - Approving clean reports that passed all validations
    - Rejecting reports with critical compliance issues
    - Updating regulatory compliance tracking systems
    - Triggering bank notifications about report status
    
    Review workflow:
    1. Use get_reports() to identify pending reports (is_accepted=null)
    2. Use get_report_errors() to review any validation issues
    3. Add comments using add_error_comment() as needed
    4. Make final accept/reject decision using this tool
    5. Bank receives notification of decision and any error comments
    
    Important considerations:
    - Acceptance indicates regulatory compliance approval
    - Rejection requires banks to resubmit corrected reports
    - Decision becomes part of permanent regulatory record
    - Status changes may trigger automated compliance workflows
    
    Note: Ensure thorough review of all errors and comments before making final decisions.
    Accepted reports are considered compliant for regulatory purposes.
    """
    token = get_latest_token()
    if not token:
        return {"error": "No active session found"}
    try:
        response = requests.put(f"{BASE_URL}/api/reports/{report_id}/status", json={"is_accepted": is_accepted}, headers={"Authorization": f"Bearer {token}"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def create_bank(aba_code: str, name: str) -> Dict[str, Any]:
    """Create a new bank in the BMO system.
    
    This tool allows BMO analysts to register a new bank that will be monitored by the organization.
    The bank will be added to the system's database and can then submit reports for validation.
    
    Parameters:
    - aba_code: The American Bankers Association (ABA) routing number for the bank. 
                This is a unique 9-digit code that identifies the financial institution.
                Example: "021000021" for JPMorgan Chase Bank
    - name: The full legal name of the bank as registered with regulatory authorities.
            Example: "JPMorgan Chase Bank, N.A."
    
    Returns:
    - success: True if bank was created successfully
    - error: Error message if creation failed (e.g., duplicate ABA code)
    
    Use cases:
    - Adding new banks that need to be monitored by BMO
    - Registering banks that will start submitting regulatory reports
    - Expanding the list of financial institutions under BMO oversight
    """
    token = get_latest_token()
    if not token:
        return {"error": "No active session found"}
    try:
        response = requests.post(f"{BASE_URL}/api/banks", 
                               json={"aba_code": aba_code, "name": name}, 
                               headers={"Authorization": f"Bearer {token}"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def update_bank(bank_id: int, aba_code: str, name: str) -> Dict[str, Any]:
    """Update an existing bank's information in the BMO system.
    
    This tool allows BMO analysts to modify bank details when there are changes to the bank's
    registration information, name changes due to mergers/acquisitions, or corrections to data.
    
    Parameters:
    - bank_id: The unique internal ID of the bank to update. Use get_banks() to find the correct ID.
    - aba_code: The updated ABA routing number. Must be a valid 9-digit ABA code.
                Example: "021000021"
    - name: The updated full legal name of the bank.
            Example: "JPMorgan Chase Bank, N.A." (after merger/name change)
    
    Returns:
    - success: True if bank was updated successfully
    - error: Error message if update failed (e.g., bank not found, invalid ABA code)
    
    Use cases:
    - Correcting bank name after corporate restructuring or mergers
    - Updating ABA codes when banks change their routing numbers
    - Fixing data entry errors in bank information
    - Maintaining accurate bank records for regulatory compliance
    
    Note: Before updating, use get_banks() to retrieve current bank information and confirm the bank_id.
    """
    token = get_latest_token()
    if not token:
        return {"error": "No active session found"}
    try:
        response = requests.put(f"{BASE_URL}/api/banks/{bank_id}", 
                              json={"aba_code": aba_code, "name": name}, 
                              headers={"Authorization": f"Bearer {token}"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def delete_bank(bank_id: int) -> Dict[str, Any]:
    """Delete a bank from the BMO system.
    
    This tool removes a bank from the BMO monitoring system. This is a permanent action that
    should be used carefully. Banks can only be deleted if they have no associated reports
    in the system to maintain data integrity and audit trails.
    
    Parameters:
    - bank_id: The unique internal ID of the bank to delete. Use get_banks() to find the correct ID.
    
    Returns:
    - success: True if bank was deleted successfully
    - error: Detailed error message if deletion failed, including:
             * "Cannot delete bank. It has X associated report(s)." - when bank has reports
             * "Bank not found" - when bank_id doesn't exist
             * Authentication errors if session is invalid
    
    Use cases:
    - Removing banks that are no longer under BMO oversight
    - Cleaning up duplicate or test bank entries
    - Removing banks that have ceased operations (only if no historical reports exist)
    
    Important restrictions:
    - Banks with existing reports cannot be deleted to preserve audit trails
    - This maintains referential integrity in the database
    - Historical reporting data is protected from accidental deletion
    
    Workflow:
    1. Use get_banks() to find the bank and confirm the bank_id
    2. Check if bank has reports using get_reports() filtered by bank name
    3. Only proceed with deletion if no reports exist
    4. Consider archiving instead of deleting for banks with historical data
    
    Note: If deletion fails due to associated reports, consider whether the bank
    should be marked as inactive rather than deleted to preserve historical data.
    """
    token = get_latest_token()
    if not token:
        return {"error": "No active session found"}
    try:
        response = requests.delete(f"{BASE_URL}/api/banks/{bank_id}", 
                                 headers={"Authorization": f"Bearer {token}"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def send_chat_message(message: str) -> Dict[str, Any]:
    """Send messages through the BMO internal communication system.
    
    This tool enables analysts to communicate within the BMO system, share information
    about reports, coordinate review activities, and maintain communication logs.
    
    Parameters:
    - message: Text message to send. Should be professional and relevant to BMO operations.
    
    Returns:
    - success: True if message was sent successfully
    - error: Error message if sending failed
    
    Use cases:
    - Coordinating report reviews between analysts
    - Sharing insights about validation patterns or issues
    - Requesting supervisor guidance on complex cases
    - Broadcasting system updates or policy changes
    - Documenting inter-team communications
    
    Message guidelines:
    - Keep messages professional and work-related
    - Include relevant report IDs or bank names when discussing specific cases
    - Use clear, concise language for effective communication
    - Follow organizational communication policies
    
    Example messages:
    - "Report R2025-001 from First National Bank requires supervisor review"
    - "Seeing pattern of date format errors from regional banks - training needed?"
    - "System maintenance scheduled for tonight 11 PM - 2 AM EST"
    - "New validation rule for crypto holdings effective next quarter"
    
    Note: Messages are logged and may be subject to compliance monitoring and audit requirements.
    """
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
    
