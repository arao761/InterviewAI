"""
Main FastAPI application entry point for PrepWise Backend.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.utils.exceptions import PrepWiseException
from app.utils.error_handlers import prepwise_exception_handler, general_exception_handler
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
    logger.info(f"CORS origins: {settings.cors_origins_list}")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME} API")


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
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
app.add_exception_handler(PrepWiseException, prepwise_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include API routes
from app.api.routes import resume, sessions, responses
app.include_router(resume.router, prefix="/api/v1")
app.include_router(sessions.router, prefix="/api/v1")
app.include_router(responses.router, prefix="/api/v1")


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