"""
API package initialization.
"""
from fastapi import APIRouter
from app.api.routes import ai_router, auth_router, payments_router, dashboard_router

# Create main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(auth_router)
api_router.include_router(payments_router)
api_router.include_router(dashboard_router)
api_router.include_router(ai_router)

__all__ = ["api_router"]
