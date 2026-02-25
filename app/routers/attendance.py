from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from datetime import date, datetime
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/attendance", tags=["attendance"])


@router.post("/", response_model=schemas.Attendance, status_code=status.HTTP_201_CREATED)
def mark_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    # First, make sure the employee actually exists
    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == attendance.employee_id
    ).first()
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID '{attendance.employee_id}' not found"
        )
    
    # Check if attendance was already marked for this date
    existing_attendance = db.query(models.Attendance).filter(
        models.Attendance.employee_id == attendance.employee_id,
        models.Attendance.date == attendance.date
    ).first()
    
    if existing_attendance:
        # Update instead of creating duplicate - this is intentional behavior
        existing_attendance.status = attendance.status
        db.commit()
        db.refresh(existing_attendance)
        return existing_attendance
    
    # All good, create new attendance record
    db_attendance = models.Attendance(**attendance.model_dump())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    
    return db_attendance


@router.get("/", response_model=List[schemas.AttendanceWithEmployee])
def get_all_attendance(
    date_filter: Optional[date] = Query(None, description="Filter by specific date"),
    employee_id: Optional[str] = Query(None, description="Filter by employee ID"),
    db: Session = Depends(get_db)
):
    query = db.query(
        models.Attendance,
        models.Employee.full_name
    ).join(models.Employee, models.Attendance.employee_id == models.Employee.employee_id)
    
    if date_filter:
        query = query.filter(models.Attendance.date == date_filter)
    
    if employee_id:
        query = query.filter(models.Attendance.employee_id == employee_id)
    
    results = query.order_by(models.Attendance.date.desc()).all()
    
    attendance_list = []
    for attendance, employee_name in results:
        attendance_dict = {
            "id": attendance.id,
            "employee_id": attendance.employee_id,
            "date": attendance.date,
            "status": attendance.status,
            "employee_name": employee_name
        }
        attendance_list.append(attendance_dict)
    
    return attendance_list


@router.get("/{employee_id}", response_model=List[schemas.Attendance])
def get_employee_attendance(employee_id: str, db: Session = Depends(get_db)):
    # verify employee exists
    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == employee_id
    ).first()
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID '{employee_id}' not found"
        )
    
    attendance_records = db.query(models.Attendance).filter(
        models.Attendance.employee_id == employee_id
    ).order_by(models.Attendance.date.desc()).all()
    
    return attendance_records


@router.delete("/{attendance_id}", response_model=schemas.MessageResponse)
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    attendance = db.query(models.Attendance).filter(
        models.Attendance.id == attendance_id
    ).first()
    
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendance record with ID '{attendance_id}' not found"
        )
    
    db.delete(attendance)
    db.commit()
    
    return {"message": "Attendance record deleted successfully"}


@router.get("/date/{date_param}", response_model=List[schemas.AttendanceWithEmployee])
def get_attendance_by_date(date_param: date, db: Session = Depends(get_db)):
    """Get all attendance records for a specific date"""
    results = db.query(
        models.Attendance,
        models.Employee.full_name
    ).join(models.Employee, models.Attendance.employee_id == models.Employee.employee_id
    ).filter(models.Attendance.date == date_param
    ).order_by(models.Employee.full_name).all()
    
    attendance_list = []
    for attendance, employee_name in results:
        attendance_dict = {
            "id": attendance.id,
            "employee_id": attendance.employee_id,
            "date": attendance.date,
            "status": attendance.status,
            "employee_name": employee_name
        }
        attendance_list.append(attendance_dict)
    
    return attendance_list


@router.get("/today/present-count", response_model=schemas.TodayPresentCountResponse)
def get_today_present_count(db: Session = Depends(get_db)):
    """Get count of present and absent employees for today"""
    today = date.today()
    
    total_employees = db.query(models.Employee).count()
    
    present_count = db.query(models.Attendance).filter(
        models.Attendance.date == today,
        models.Attendance.status == models.AttendanceStatus.PRESENT
    ).count()
    
    absent_count = db.query(models.Attendance).filter(
        models.Attendance.date == today,
        models.Attendance.status == models.AttendanceStatus.ABSENT
    ).count()
    
    return {
        "date": today,
        "present_count": present_count,
        "absent_count": absent_count,
        "total_employees": total_employees
    }


@router.get("/monthly-report/{year}/{month}", response_model=schemas.MonthlyReportResponse)
def get_monthly_attendance_report(
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    """Get monthly attendance report for all employees"""
    # Validate year and month
    if year < 2000 or year > 2100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Year must be between 2000 and 2100"
        )
    
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Month must be between 1 and 12"
        )
    
    # Get all employees
    employees = db.query(models.Employee).all()
    
    report_data = []
    for employee in employees:
        # Count present and absent days for this employee in the specified month
        attendance_records = db.query(models.Attendance).filter(
            models.Attendance.employee_id == employee.employee_id,
            extract('year', models.Attendance.date) == year,
            extract('month', models.Attendance.date) == month
        ).all()
        
        present_days = sum(1 for record in attendance_records if record.status == models.AttendanceStatus.PRESENT)
        absent_days = sum(1 for record in attendance_records if record.status == models.AttendanceStatus.ABSENT)
        total_days = len(attendance_records)
        
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0.0
        
        report_data.append({
            "employee_id": employee.employee_id,
            "employee_name": employee.full_name,
            "total_days": total_days,
            "present_days": present_days,
            "absent_days": absent_days,
            "attendance_percentage": round(attendance_percentage, 2)
        })
    
    return {
        "year": year,
        "month": month,
        "report": report_data
    }

