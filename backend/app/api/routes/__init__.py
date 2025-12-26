"""
API Routes initialization.
"""
from app.api.routes.ai_routes import router as ai_router
from app.api.routes.auth import router as auth_router
from app.api.routes.payments import router as payments_router

__all__ = ["ai_router", "auth_router", "payments_router"]
