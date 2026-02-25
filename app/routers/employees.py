from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/employees", tags=["employees"])


@router.post("/", response_model=schemas.Employee, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    # Make sure employee_id doesn't already exist
    existing_employee = db.query(models.Employee).filter(
        models.Employee.employee_id == employee.employee_id
    ).first()
    
    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Employee with ID '{employee.employee_id}' already exists"
        )
    
    # Also check if email is already taken
    existing_email = db.query(models.Employee).filter(
        models.Employee.email == employee.email
    ).first()
    
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Employee with email '{employee.email}' already exists"
        )
    
    # All good, create the employee
    try:
        db_employee = models.Employee(**employee.model_dump())
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create employee due to duplicate values"
        )


@router.get("/", response_model=List[schemas.Employee])
def get_all_employees(db: Session = Depends(get_db)):
    employees = db.query(models.Employee).all()
    return employees


@router.get("/{employee_id}", response_model=schemas.EmployeeWithAttendance)
def get_employee(employee_id: str, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == employee_id
    ).first()
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID '{employee_id}' not found"
        )
    
    # get total present days
    total_present = db.query(models.Attendance).filter(
        models.Attendance.employee_id == employee_id,
        models.Attendance.status == models.AttendanceStatus.PRESENT
    ).count()
    
    employee_dict = {
        "id": employee.id,
        "employee_id": employee.employee_id,
        "full_name": employee.full_name,
        "email": employee.email,
        "department": employee.department,
        "total_present_days": total_present,
        "attendance_records": employee.attendance_records
    }
    
    return employee_dict


@router.delete("/{employee_id}", response_model=schemas.MessageResponse)
def delete_employee(employee_id: str, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == employee_id
    ).first()
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID '{employee_id}' not found"
        )
    
    db.delete(employee)
    db.commit()
    
    return {"message": f"Employee '{employee.full_name}' deleted successfully"}


@router.get("/stats/count", response_model=schemas.EmployeeCountResponse)
def get_employees_count(db: Session = Depends(get_db)):
    """Get total count of employees in the system"""
    total_employees = db.query(models.Employee).count()
    
    return {"total_employees": total_employees}

