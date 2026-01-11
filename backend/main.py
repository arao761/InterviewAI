"""
Main FastAPI application entry point for PrepWise Backend.

SECURITY FEATURES:
- Rate limiting on all endpoints (OWASP API4:2023)
- CORS protection with whitelist
- Input validation via Pydantic schemas
- JWT authentication with secure token handling
- Security headers for XSS/clickjacking prevention
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.utils.exceptions import PrepWiseException
from app.utils.error_handlers import prepwise_exception_handler, general_exception_handler
from app.api import api_router
from app.core.cache import cache_manager
from app.middleware.rate_limit import RateLimitMiddleware
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    logger.info(f"Starting {settings.APP_NAME} API v{settings.API_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Host: {settings.HOST}:{settings.PORT}")
    logger.info(f"CORS origins: {settings.cors_origins_list}")
    
    # Initialize Redis cache
    logger.info("Initializing Redis cache...")
    await cache_manager.connect()

    # Verify PrepWise AI is available
    try:
        from app.services.ai_service import AIService
        logger.info("✅ PrepWise AI module loaded successfully")
        # Try to initialize AI service
        test_service = AIService()
        logger.info("✅ AIService initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize AIService: {e}")
        logger.error("⚠️  AI features may not work properly")
        logger.error("💡 Make sure to run: cd backend && pip install -e ../ai-engine")

    yield

    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME} API")
    await cache_manager.close()


# Create FastAPI app instance
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered interview preparation platform with resume parsing, mock interviews, and real-time feedback",
    version=settings.API_VERSION,
    debug=settings.DEBUG,
    docs_url=f"/api/{settings.API_VERSION}/docs",
    redoc_url=f"/api/{settings.API_VERSION}/redoc",
    openapi_url=f"/api/{settings.API_VERSION}/openapi.json",
    lifespan=lifespan,
)

# ============================================================================
# SECURITY MIDDLEWARE CONFIGURATION (OWASP Best Practices)
# ============================================================================

# 1. Rate Limiting Middleware - MUST be first to prevent abuse
# Implements OWASP API4:2023 - Unrestricted Resource Consumption
app.add_middleware(RateLimitMiddleware)

# 2. CORS Configuration - Restrict origins in production
# SECURITY NOTE: "*" allows all origins - only use in development
# In production, explicitly list allowed origins in CORS_ORIGINS env variable
cors_origins = settings.cors_origins_list if settings.cors_origins_list else ["*"]
if "*" in cors_origins and settings.ENVIRONMENT == "production":
    logger.warning("⚠️  CORS is set to allow all origins in PRODUCTION. This is a security risk!")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],  # Explicit methods only
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Window"],
)

# 3. Trusted Host Middleware - Prevent Host Header attacks
# Only in production to avoid localhost issues in development
if settings.ENVIRONMENT == "production" and settings.TRUSTED_HOSTS:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.TRUSTED_HOSTS.split(",")
    )

# Add exception handlers
app.add_exception_handler(PrepWiseException, prepwise_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include API routes
app.include_router(api_router, prefix=f"/api/{settings.API_VERSION}")


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: Status and application information
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT,
    }


# ============================================================================
# SECURITY HEADERS (OWASP Best Practices)
# ============================================================================
@app.middleware("http")
async def add_security_headers(request, call_next):
    """
    Add security headers to all responses.

    OWASP Security Headers:
    - X-Content-Type-Options: Prevent MIME sniffing
    - X-Frame-Options: Prevent clickjacking
    - X-XSS-Protection: Enable XSS filter
    - Strict-Transport-Security: Enforce HTTPS (production only)
    - Content-Security-Policy: Prevent XSS attacks
    - Referrer-Policy: Control referrer information
    """
    response = await call_next(request)

    # Prevent MIME type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"

    # Prevent clickjacking attacks
    response.headers["X-Frame-Options"] = "DENY"

    # Enable XSS filtering (legacy browsers)
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # Content Security Policy - for API responses only
    # NOTE: This CSP applies to backend API responses (JSON). Your Next.js frontend
    # has its own CSP configuration in next.config.mjs for browser security.
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )

    # Control referrer information
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # Permissions policy (formerly Feature-Policy)
    response.headers["Permissions-Policy"] = (
        "geolocation=(), microphone=(), camera=(), payment=()"
    )

    # HSTS - Force HTTPS in production
    # SECURITY NOTE: Only enable in production with valid SSL certificate
    if settings.ENVIRONMENT == "production":
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains; preload"
        )

    return response


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.

    Returns:
        dict: Welcome message and documentation links
    """
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.API_VERSION,
        "docs": f"/api/{settings.API_VERSION}/docs",
        "redoc": f"/api/{settings.API_VERSION}/redoc",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS,
    )