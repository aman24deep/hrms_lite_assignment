from sqlalchemy import Column, String, Integer, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum


# Enum for attendance status - only two options for now
class AttendanceStatus(str, enum.Enum):
    PRESENT = "Present"
    ABSENT = "Absent"


class Employee(Base):
    """Employee model - stores basic employee information"""
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True, nullable=False)  # Like EMP001
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    department = Column(String, nullable=False)
    
    # Relationship: one employee has many attendance records
    # cascade="all, delete-orphan" means if we delete an employee, delete their attendance too
    attendance_records = relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")


class Attendance(Base):
    """Attendance model - tracks daily attendance for employees"""
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)
    
    # Relationship back to employee
    employee = relationship("Employee", back_populates="attendance_records")
