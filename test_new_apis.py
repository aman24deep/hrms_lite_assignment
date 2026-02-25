"""
Testing the new reporting and stats endpoints.
Run this after you've got some test data in the database.
"""
import requests
from datetime import date

BASE_URL = "http://localhost:8000"

def test_get_attendance_by_date():
    """Test: Get all attendance for a particular date"""
    print("\n1. Testing: Get attendance by date (2026-02-25)...")
    today_date = str(date.today())
    response = requests.get(f"{BASE_URL}/api/attendance/date/{today_date}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_get_today_present_count():
    """Test: Get today's present employees count"""
    print("\n2. Testing: Get today's present count...")
    response = requests.get(f"{BASE_URL}/api/attendance/today/present-count")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_get_monthly_report():
    """Test: Get monthly attendance report"""
    print("\n3. Testing: Get monthly attendance report (Feb 2026)...")
    response = requests.get(f"{BASE_URL}/api/attendance/monthly-report/2026/2?year=2026&month=2")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_get_employees_count():
    """Test: Get total employees count"""
    print("\n4. Testing: Get total employees count...")
    response = requests.get(f"{BASE_URL}/api/employees/stats/count")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    print("=" * 60)
    print("Testing New API Endpoints")
    print("=" * 60)
    
    test_get_attendance_by_date()
    test_get_today_present_count()
    test_get_monthly_report()
    test_get_employees_count()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
