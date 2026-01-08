from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/clash_royale_analyzer"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # File Upload
    MAX_UPLOAD_SIZE: int = 524288000  # 500MB
    UPLOAD_DIR: str = "./uploads"
    PROCESSED_DIR: str = "./processed"

    # ML Models
    CARD_DETECTION_MODEL: str = "./models/card_detector.pt"
    GAME_ENGINE_MODEL: str = "./models/game_engine.pt"

    # Video Processing
    FPS_SAMPLE_RATE: int = 2  # Process 2 frames per second
    VIDEO_RESOLUTION: tuple = (1280, 720)

    # Game Analysis
    ELIXIR_REGEN_RATE: float = 1.0  # Elixir per second
    MAX_ELIXIR: int = 10
    OVERTIME_ELIXIR_RATE: float = 2.0

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
