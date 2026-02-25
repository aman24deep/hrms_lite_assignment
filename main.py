from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine, Base
from app.routers import employees, attendance
from app.config import settings

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

# Enhanced API documentation for Swagger
app = FastAPI(
    title="HRMS_LITE APIs",
    description="""
    ## Employee Attendance System API
    
    A comprehensive REST API for managing employee records and tracking attendance.
    
    ### Features
    
    * **Employee Management** - Create, read, update, and delete employees
    * **Attendance Tracking** - Mark and track daily attendance (Present/Absent)
    * **Reporting** - Generate attendance reports and statistics
    * **Real-time Stats** - Get employee counts and today's attendance
    
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "amandeep.contact.me@gmail.com",
    },
    docs_url="/swagger",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
    openapi_url="/openapi.json",  # OpenAPI schema
)

# Enable CORS so frontend can talk to this API
# TODO: In production, replace "*" with your actual frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For now allowing all origins during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom error handler to make validation errors more readable
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        errors.append(f"{field}: {message}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": errors}
    )


# Handle database errors gracefully
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database error occurred. Please try again later."}
    )


app.include_router(employees.router)
app.include_router(attendance.router)


# OpenAPI tags metadata for better Swagger organization
tags_metadata = [
    {
        "name": "employees",
        "description": "Operations related to employee management. Create, retrieve, update, and delete employee records.",
    },
    {
        "name": "attendance",
        "description": "Operations for tracking and managing employee attendance. Mark attendance, generate reports, and view statistics.",
    },
]



