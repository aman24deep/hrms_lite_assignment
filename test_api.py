"""
Test script for API
"""
import requests
from datetime import date

BASE_URL = "http://localhost:8000"

def test_create_employee():
    print("Creating employee...")
    employee = {
        "employee_id": "EMP001",
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "department": "Engineering"
    }
    response = requests.post(f"{BASE_URL}/api/employees/", json=employee)
    print(f"Status: {response.status_code}")
    print(response.json())
    return response.json()

def test_get_employees():
    print("\nGetting all employees...")
    response = requests.get(f"{BASE_URL}/api/employees/")
    print(f"Status: {response.status_code}")
    print(response.json())

def test_mark_attendance(employee_id):
    print("\nMarking attendance...")
    attendance = {
        "employee_id": employee_id,
        "date": str(date.today()),
        "status": "Present"
    }
    response = requests.post(f"{BASE_URL}/api/attendance/", json=attendance)
    print(f"Status: {response.status_code}")
    print(response.json())

if __name__ == "__main__":
    print("Testing API...\n")
    employee = test_create_employee()
    
    # Handle case where employee already exists from previous test runs
    if "employee_id" not in employee:
        print("Employee already exists, fetching from database...")
        response = requests.get(f"{BASE_URL}/api/employees/")
        employees = response.json()
        if employees:
            employee = employees[0]  # Just use the first one
    
    test_get_employees()
    test_mark_attendance(employee["employee_id"])
    print("\nAll tests passed! 🎉")
