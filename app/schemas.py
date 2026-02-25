from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import date
from enum import Enum
from typing import List, Optional

# Pydantic schemas for request/response validation
# These define what data we expect from the client and what we send back

class AttendanceStatus(str, Enum):
    PRESENT = "Present"
    ABSENT = "Absent"


# Base schema with common employee fields
class EmployeeBase(BaseModel):
    employee_id: str = Field(..., min_length=1)  # Required, at least 1 character
    full_name: str = Field(..., min_length=1)
    email: EmailStr  # Pydantic validates email format automatically
    department: str = Field(..., min_length=1)


# For creating new employees - same as base for now
class EmployeeCreate(EmployeeBase):
    pass


# Response schema - includes the database ID
class Employee(EmployeeBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)  # Allows creating from SQLAlchemy models


class AttendanceBase(BaseModel):
    employee_id: str
    date: date
    status: AttendanceStatus


class AttendanceCreate(AttendanceBase):
    pass


class Attendance(AttendanceBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class AttendanceWithEmployee(Attendance):
    employee_name: str
    
    model_config = ConfigDict(from_attributes=True)


class EmployeeWithAttendance(Employee):
    total_present_days: Optional[int] = None
    attendance_records: List[Attendance] = []
    
    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BaseModel):
    detail: str


class MessageResponse(BaseModel):
    message: str


class EmployeeCountResponse(BaseModel):
    total_employees: int


class TodayPresentCountResponse(BaseModel):
    date: date
    present_count: int
    absent_count: int
    total_employees: int


class MonthlyAttendanceReport(BaseModel):
    employee_id: str
    employee_name: str
    total_days: int
    present_days: int
    absent_days: int
    attendance_percentage: float


class MonthlyReportResponse(BaseModel):
    year: int
    month: int
    report: List[MonthlyAttendanceReport]
