from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    role: str

class Bank(BaseModel):
    id: int
    aba_code: str
    name: str

class Report(BaseModel):
    id: int
    bank_id: int
    bank_name: str
    aba_code: str
    report_code: str
    submission_date: str
    has_errors: bool
    is_accepted: Optional[bool]

class ValidationError(BaseModel):
    id: int
    report_id: int
    error_type: str
    error_message: str
    field_name: Optional[str]

class ErrorComment(BaseModel):
    id: int
    error_id: int
    user_id: int
    username: str
    comment: str
    created_at: str

class CommentRequest(BaseModel):
    comment: str

class StatusUpdateRequest(BaseModel):
    is_accepted: bool