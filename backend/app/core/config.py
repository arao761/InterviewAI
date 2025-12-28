from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./app.db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "prepwise_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"

    # FastAPI Configuration
    APP_NAME: str = "PrepWise API"
    APP_VERSION: str = "1.0.0"
    API_VERSION: str = "v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # File Upload Configuration
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_FILE_TYPES: str = "pdf,doc,docx"
    UPLOAD_DIR: str = "./uploads"

    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"

    # AI/NLP Configuration
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""  # Optional
    AI_MODEL: str = "gpt-4"
    AI_TEMPERATURE: float = 0.7

    # Stripe Configuration
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRICE_STARTER: str = ""  # Stripe Price ID for Starter plan
    STRIPE_PRICE_PROFESSIONAL: str = ""  # Stripe Price ID for Professional plan

    # Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""  # Your email address
    SMTP_PASSWORD: str = ""  # Your email password or app password
    FROM_EMAIL: str = ""  # Sender email (defaults to SMTP_USER)
    FRONTEND_URL: str = "http://localhost:3000"  # Frontend URL for verification links

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        extra = "allow"  # Changed from "ignore" to "allow"


settings = Settings()