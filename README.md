# Employee Attendance Management System - Backend

A REST API built for tracking employee attendance and generating reports. This started as a simple CRUD app but evolved to include some useful reporting features.

## Project Overview

This is the backend service for an employee attendance management system. The main idea is pretty simple - HR or managers can add employees to the system, mark their daily attendance (Present/Absent), and pull various reports.

**What you can do with this API:**

**Employee Management**
- Add new employees with unique IDs and email addresses
- View all employees or search for specific ones
- Get detailed employee profiles including their full attendance history
- Delete employees (this also removes all their attendance records)

**Attendance Tracking**
- Mark daily attendance as Present or Absent
- Update attendance if you accidentally marked it wrong (won't create duplicates)
- View attendance records with multiple filtering options
- Get attendance for a specific date to see who was present/absent that day

**Reports & Statistics**
- Get total employee count
- See today's attendance summary (how many present vs absent)
- Generate monthly attendance reports with percentages for each employee
- View individual employee attendance history

I built this to be simple but flexible enough to cover the basic needs of a small to medium organization.

## Tech Stack

Here's what I used to build this:

- **FastAPI** - Python web framework for building APIs. Chose this because it's really fast, has automatic API documentation (Swagger UI), and great data validation
- **PostgreSQL** - Relational database. Using Supabase for hosting because it's free and easy to set up
- **SQLAlchemy** - Python SQL toolkit and ORM. Makes database operations much cleaner than writing raw SQL
- **Pydantic** - Data validation using Python type hints. Works seamlessly with FastAPI
- **Uvicorn** - ASGI server to run the application
- **python-dotenv** - For managing environment variables
- **psycopg2-binary** - PostgreSQL adapter for Python

All packages and versions are in `requirements.txt`.

## How to Run This Project Locally

### Prerequisites

Before you start, make sure you have these installed:
- **Python 3.8+** (I'm using 3.11, but anything 3.8 or above should work)
- **PostgreSQL** (or you can use a cloud database like Supabase - explained below)
- **Git** (to clone the repository)

### Step-by-Step Setup

**Step 1: Clone the repository**

```bash
git clone <https://github.com/aman24deep/hrms_lite_assignment.git>
cd AssignmentBackend
```

**Step 2: Create a virtual environment**

This keeps your project dependencies isolated from other Python projects.

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt now.

**Step 3: Install dependencies**

```bash
pip install -r requirements.txt
```

This will install FastAPI, SQLAlchemy, PostgreSQL driver, and all other needed packages.

**Step 4: Set up your database**

You have two options here:

**Option A: Local PostgreSQL**

If you have PostgreSQL installed locally:

```bash
# Open PostgreSQL command line
psql -U postgres

# Create a database
CREATE DATABASE hrms_db;

# Exit psql
\q
```

Your DATABASE_URL will be: `postgresql://postgres:your_password@localhost:5432/hrms_db`

**Option B: Use Supabase (Recommended for quick setup)**

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project
3. Go to Project Settings → Database
4. Copy the "Connection string" under "Connection pooling"
5. Replace `[YOUR-PASSWORD]` with your actual database password

**Step 5: Configure environment variables**

Create a `.env` file in the root directory of the project:

```bash
# On Windows
type nul > .env

# On Mac/Linux
touch .env
```

Open `.env` in your text editor and add:

```env
DATABASE_URL=postgresql://user:password@host:5432/database_name
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

Replace the `DATABASE_URL` with your actual database connection string.

**Step 6: Run the application**

**Step 6: Run the application**

```bash
uvicorn main:app --reload
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

**Step 7: Explore the Interactive API Documentation (Swagger)**

FastAPI automatically generates interactive API documentation. Open your browser and visit:

- **Swagger UI**: http://localhost:8000/docs 
  - Interactive interface where you can test all endpoints
  - Click "Try it out" to execute API calls directly from your browser
  - See request/response examples for each endpoint
  
- **ReDoc**: http://localhost:8000/redoc 
  - Alternative documentation style
  - Better for reading and understanding the API structure
  
- **OpenAPI Schema**: http://localhost:8000/openapi.json 
  - Raw OpenAPI specification in JSON format

### Quick Test

You can run the included test scripts to make sure everything works:

```bash
# Test database connection
python test_db.py

# Test the API endpoints
python test_api.py

# Test the reporting features
python test_new_apis.py
```

If you see "✓ Database connected successfully!" and API responses with status 200/201, you're good to go!

### Troubleshooting

**Database connection errors?**
- Double-check your DATABASE_URL in the `.env` file
- Make sure PostgreSQL is running (if using local database)
- Check if you can connect to Supabase from your network

**Module not found errors?**
- Make sure your virtual environment is activated
- Run `pip install -r requirements.txt` again

**Port already in use?**
- Another app might be using port 8000
- Run with a different port: `uvicorn main:app --reload --port 8080`

## Interactive API Documentation (Swagger UI)

This project includes **auto-generated interactive API documentation** powered by FastAPI and Swagger UI.

### Accessing Swagger UI

Once your server is running, visit: **http://localhost:8000/docs**

### Features

**🎯 Interactive Testing**
- Click any endpoint to expand it
- Click "Try it out" button
- Fill in the parameters
- Click "Execute" to make a real API call
- See the response in real-time

**📝 Request/Response Examples**
- View request body schemas
- See example values for each field
- Understand required vs optional parameters
- View all possible response codes

**🔍 Schema Explorer**
- Browse all data models
- See field types and validation rules
- Understand the data structure

**🎨 User-Friendly Interface**
- Organized by tags (Employees, Attendance)
- Dark theme for code syntax
- Collapsible sections
- Search functionality

### Alternative Documentation

- **ReDoc** (http://localhost:8000/redoc) - Cleaner, read-only documentation
- **OpenAPI JSON** (http://localhost:8000/openapi.json) - Raw API specification

### Quick Start with Swagger

1. Navigate to http://localhost:8000/docs
2. Find the "POST /api/employees/" endpoint
3. Click "Try it out"
4. Use this example data:
```json
{
  "employee_id": "EMP001",
  "full_name": "John Doe",
  "email": "john@example.com",
  "department": "Engineering"
}
```
5. Click "Execute"
6. See the response with status 201!

## API Endpoints

You can test all these endpoints using the Swagger UI at http://localhost:8000/docs

### Employee Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/employees/` | Create a new employee |
| GET | `/api/employees/` | Get list of all employees |
| GET | `/api/employees/{employee_id}` | Get a specific employee with attendance stats |
| GET | `/api/employees/stats/count` | Get total employee count |
| DELETE | `/api/employees/{employee_id}` | Remove an employee |

**Example - Create Employee:**
```json
POST /api/employees/
{
  "employee_id": "EMP001",
  "full_name": "John Doe",
  "email": "john.doe@company.com",
  "department": "Engineering"
}
```

### Attendance Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/attendance/` | Mark attendance for an employee |
| GET | `/api/attendance/` | Get all attendance records (supports filters) |
| GET | `/api/attendance/date/{date}` | Get attendance for a specific date |
| GET | `/api/attendance/{employee_id}` | Get attendance history for one employee |
| GET | `/api/attendance/today/present-count` | Get today's attendance summary |
| GET | `/api/attendance/monthly-report/{year}/{month}` | Generate monthly report |
| DELETE | `/api/attendance/{attendance_id}` | Delete an attendance record |

**Example - Mark Attendance:**
```json
POST /api/attendance/
{
  "employee_id": "EMP001",
  "date": "2026-02-25",
  "status": "Present"
}
```

**Query Parameters:**
- `GET /api/attendance/?date_filter=2026-02-25` - Filter by date
- `GET /api/attendance/?employee_id=EMP001` - Filter by employee

## Database Schema

The database has two main tables with a one-to-many relationship:

**employees**
- `id` - Primary key (auto-increment)
- `employee_id` - Unique identifier (e.g., "EMP001")
- `full_name` - Employee name
- `email` - Unique email address
- `department` - Department name

**attendance**
- `id` - Primary key (auto-increment)
- `employee_id` - Foreign key to employees table
- `date` - Date of attendance
- `status` - Either "Present" or "Absent"

**Relationship**: One employee can have many attendance records. When you delete an employee, all their attendance records are automatically deleted (cascade delete).

## Project Structure

```
AssignmentBackend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings and environment variables
│   ├── database.py          # Database connection and session
│   ├── models.py            # SQLAlchemy models (database tables)
│   ├── schemas.py           # Pydantic schemas (validation)
│   └── routers/
│       ├── __init__.py
│       ├── employees.py     # Employee-related endpoints
│       └── attendance.py    # Attendance-related endpoints
├── test_api.py              # Basic API tests
├── test_db.py               # Database connection test
├── test_new_apis.py         # Tests for reporting endpoints
├── requirements.txt         # Python dependencies
├── runtime.txt              # Python version for deployment
├── Procfile                 # Heroku/Render deployment config
├── .env                     # Environment variables (not in git)
└── README.md                # This file
```

## Deployment

The app is ready to deploy on platforms like Render, Railway, or Heroku.

### Deploy on Render.com

1. Create a PostgreSQL database on Render (free tier available)
2. Copy the internal database URL
3. Create a new Web Service from your GitHub repo
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - `DATABASE_URL` - your database URL
   - `CORS_ORIGINS` - your frontend URL

### Deploy on Railway.app

1. Create new project from GitHub
2. Add PostgreSQL plugin (auto-configures DATABASE_URL)
3. Add `CORS_ORIGINS` environment variable
4. Deploy automatically

The `Procfile` and `runtime.txt` files are already configured for deployment.

## Assumptions & Limitations

Here are some things to be aware of:

### Assumptions Made

1. **Employee IDs are managed manually** - The system doesn't auto-generate employee IDs like "EMP001", "EMP002", etc. You need to provide unique IDs when creating employees.

2. **One attendance entry per day** - An employee can only have one attendance record per day. If you mark attendance twice for the same date, it updates the existing record instead of creating a duplicate.

3. **Only two attendance statuses** - Currently supports only "Present" and "Absent". Didn't include things like "Half Day", "On Leave", "Work From Home", etc. (but these could be easily added).

4. **No time tracking** - The system tracks attendance by date only, not specific clock-in/clock-out times.

5. **No authentication** - Currently there's no user authentication or authorization. In a production environment, you'd want to add JWT tokens or OAuth to protect these endpoints.

6. **CORS is open during development** - The API currently accepts requests from any origin (`allow_origins=["*"]`). This should be restricted to specific domains in production.

### Limitations

1. **No bulk operations** - You can't upload attendance for multiple employees at once via CSV or Excel. Each attendance entry needs to be created individually through the API.

2. **Limited reporting** - Monthly reports show basic stats (present/absent days and percentage). More advanced analytics like trends, comparisons, or forecasting aren't available.

3. **No leave management** - The system doesn't distinguish between different types of absences (sick leave, vacation, public holiday, etc.).

4. **No notifications** - There's no email or SMS notification system for attendance reminders or reports.

5. **Basic validation** - While the API validates required fields and data types, it doesn't check things like future dates, business days, or company-specific rules.

6. **No audit trail** - The system doesn't track who created or modified records, or when changes were made.

### Future Enhancements

Some things I'd like to add in the future:
- User authentication and role-based access control
- More attendance statuses (Half Day, Leave, WFH, etc.)
- Bulk attendance upload via CSV
- Email notifications for attendance reminders
- More detailed reporting (weekly reports, quarterly summaries)
- Dashboard with charts and graphs
- Leave management system
- Shift management for different work timings

## Notes

- All date formats use ISO 8601 standard (YYYY-MM-DD)
- API returns proper HTTP status codes (200, 201, 400, 404, 500)
- FastAPI automatically generates interactive API documentation
- The database schema is created automatically when you first run the app
- Error messages are descriptive to help with debugging

## Questions or Issues?

If you run into any problems or have questions, check:
1. Make sure your `.env` file is configured correctly
2. Verify your database connection
3. Check the terminal output for error messages
4. Try the test scripts to isolate the issue

The FastAPI auto-documentation at `/docs` is also really helpful for understanding what data each endpoint expects.

---

Happy coding! 🚀
