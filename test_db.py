from app.database import engine, Base
from app.models import Employee, Attendance

print("Testing database connection...")
try:
    Base.metadata.create_all(bind=engine)
    print("✓ Database connected successfully!")
    print("✓ Tables created/verified!")
except Exception as e:
    print(f"✗ Error: {e}")
