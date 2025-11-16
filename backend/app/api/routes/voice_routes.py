"""
Voice API Routes - Integration with VAPI for voice interviews
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any
import httpx
from app.core.config import settings
from app.core.logging import logger

router = APIRouter(
    prefix="/voice",
    tags=["Voice"],
    responses={
        500: {"description": "Internal server error"},
        400: {"description": "Bad request"},
    },
)

# Voice API base URL (assuming it runs on port 8001)
VOICE_API_URL = "http://localhost:8001"


@router.get("/health")
async def voice_health_check() -> Dict[str, Any]:
    """
    Check voice API health
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{VOICE_API_URL}/health")
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "healthy",
                    "voice_api": data,
                    "integration": "active"
                }
            else:
                return {
                    "status": "unhealthy",
                    "error": "Voice API not responding",
                    "integration": "inactive"
                }
    except Exception as e:
        logger.error(f"Voice API health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "integration": "inactive",
            "message": "Voice API may not be running. Start it with: cd voice-api/voice && python main.py"
        }


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(..., description="Audio file to transcribe")
) -> Dict[str, Any]:
    """
    Transcribe audio file using voice API

    Proxies request to voice-api service
    """
    try:
        # Read file content
        content = await file.read()

        # Forward to voice API
        async with httpx.AsyncClient(timeout=30.0) as client:
            files = {"file": (file.filename, content, file.content_type)}
            response = await client.post(
                f"{VOICE_API_URL}/transcribe",
                files=files
            )

            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Voice API error: {response.text}"
                )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Voice API request timed out"
        )
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}"
        )


@router.post("/start-voice-interview")
async def start_voice_interview(
    questions: list[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Initialize voice interview session with questions

    This endpoint prepares the voice API for an interview session
    """
    try:
        # Store questions for voice interview
        # In production, this would use a session store
        return {
            "success": True,
            "session_id": "voice_session_" + str(hash(str(questions))),
            "questions": questions,
            "message": "Voice interview session initialized",
            "instructions": {
                "1": "User will record audio for each question",
                "2": "Audio will be transcribed using voice API",
                "3": "Transcriptions will be evaluated using AI service"
            }
        }
    except Exception as e:
        logger.error(f"Voice interview initialization error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize voice interview: {str(e)}"
        )
