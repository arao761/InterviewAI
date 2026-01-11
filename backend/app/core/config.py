"""
Application configuration using Pydantic Settings.

SECURITY NOTES:
- All sensitive values should come from environment variables
- Never hardcode secrets in this file
- Use strong, unique values for SECRET_KEY in production
- Keep different API keys for dev/staging/production
- See .env.example for all available configuration options

For production deployment:
1. Set ENVIRONMENT=production
2. Set DEBUG=False
3. Use strong SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
4. Configure production database (PostgreSQL)
5. Set specific CORS_ORIGINS (no wildcards)
6. Use production API keys
7. Enable HTTPS
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Priority order:
    1. Environment variables
    2. .env file
    3. Default values defined here

    SECURITY: Sensitive values should NEVER have defaults.
    They should be required via environment variables.
    """
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

    # Security Configuration
    # CRITICAL: Change SECRET_KEY in production!
    # Generate secure key: python -c "import secrets; print(secrets.token_urlsafe(32))"
    # SECURITY: This default is INSECURE. Set via environment variable in production.
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"  # JWT signing algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Token lifetime

    # File Upload Configuration
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_FILE_TYPES: str = "pdf,doc,docx"
    UPLOAD_DIR: str = "./uploads"

    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # CORS - Comma-separated list of allowed origins
    # SECURITY: In production, list only trusted domains. Never use "*" in production.
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080,https://interview-ai-umber-six.vercel.app"

    # Trusted Hosts - Prevent Host Header attacks
    # SECURITY: List all domains your API should respond to
    TRUSTED_HOSTS: str = "localhost,127.0.0.1,interview-ai-umber-six.vercel.app"

    # AI/NLP Configuration
    # SECURITY: Keep these keys secret. Never expose client-side.
    # BEST PRACTICE: Enable API key restrictions (IP whitelist, usage limits) in provider dashboard
    # KEY ROTATION: Rotate every 90 days or immediately if exposed
    OPENAI_API_KEY: str = ""  # Required for AI features
    ANTHROPIC_API_KEY: str = ""  # Optional alternative provider
    AI_MODEL: str = "gpt-4"
    AI_TEMPERATURE: float = 0.7

    # Stripe Payment Configuration
    # SECURITY: Use test keys (sk_test_) in development, live keys (sk_live_) in production
    # NEVER expose secret keys client-side - only use on backend
    # KEY ROTATION: Rotate if exposed, use different keys per environment
    STRIPE_SECRET_KEY: str = ""  # Backend only - NEVER expose to client
    STRIPE_PUBLISHABLE_KEY: str = ""  # Can be public, but use domain restrictions
    STRIPE_WEBHOOK_SECRET: str = ""  # For webhook signature verification
    STRIPE_PRICE_STARTER: str = ""  # Stripe Price ID for Starter plan
    STRIPE_PRICE_PROFESSIONAL: str = ""  # Stripe Price ID for Professional plan

    # Email Configuration
    # Option 1: SMTP (e.g., Gmail with app-specific password)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""  # Email address
    SMTP_PASSWORD: str = ""  # App password (not regular password for Gmail)
    FROM_EMAIL: str = ""  # Sender email (defaults to SMTP_USER)
    FRONTEND_URL: str = "http://localhost:3000"  # For verification/reset links

    # Option 2: AWS SES (Recommended for production - more reliable, works on free tier)
    # SECURITY: Use IAM role with minimal permissions in production
    AWS_ACCESS_KEY_ID: str = ""  # AWS access key
    AWS_SECRET_ACCESS_KEY: str = ""  # AWS secret key - NEVER expose
    AWS_REGION: str = "us-east-1"
    AWS_SES_FROM_EMAIL: str = ""  # Verified sender email in AWS SES

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        extra = "allow"  # Changed from "ignore" to "allow"


settings = Settings()