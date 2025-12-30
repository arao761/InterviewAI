"""
Main FastAPI application entry point for PrepWise Backend.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.utils.exceptions import PrepWiseException
from app.utils.error_handlers import prepwise_exception_handler, general_exception_handler
from app.api import api_router
from app.core.cache import cache_manager
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

# Configure CORS
# In production, allow all origins if CORS_ORIGINS is not set or is empty
# Otherwise use the configured origins
cors_origins = settings.cors_origins_list if settings.cors_origins_list else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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