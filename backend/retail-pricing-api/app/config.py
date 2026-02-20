from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API settings
    API_DEBUG: bool = True
    API_PORT: int = 8000
    PROJECT_NAME: str = "FastAPI MySQL Integration"
    PROJECT_VERSION: str = "1.0.0"

    # Database settings
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_SERVER: str
    MYSQL_PORT: str
    MYSQL_SCHEMA: str
    DATABASE_URL: Optional[str] = None

    class Config:
        env_file = Path(__file__).resolve().parents[0] / ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **data):
        super().__init__(**data)
        self.DATABASE_URL = (
            f"python -m sqlacodegen mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_SCHEMA}"
        )

        
@lru_cache
def get_settings():
    return Settings()
