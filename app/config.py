from pydantic_settings import BaseSettings
from pydantic import ConfigDict

# Using Pydantic to manage environment variables
class Settings(BaseSettings):
    # Database URL - gets overridden by .env file if present
    database_url: str = "postgresql://postgres:postgres@localhost:5432/hrms_db"
    
    model_config = ConfigDict(
        env_file=".env",  # Load from .env file
        extra="ignore"    # Ignore extra fields in .env
    )


settings = Settings()
