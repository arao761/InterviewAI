"""
API Routes initialization.
"""
from app.api.routes.ai_routes import router as ai_router
from app.api.routes.voice_routes import router as voice_router

__all__ = ["ai_router", "voice_router"]
