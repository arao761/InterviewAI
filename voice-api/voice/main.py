from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import Config
import uvicorn
from contextlib import asynccontextmanager
from typing import Optional
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup: Validate configuration (warn but don't fail if API keys missing)
    try:
        Config.validate()
        print("✅ Configuration validated successfully")
        print(f"📊 Config summary: {Config.get_config_summary()}")
    except ValueError as e:
        print(f"⚠️  Configuration warning: {e}")
        print("⚠️  Server will start but API features requiring keys will not work")
        print("⚠️  This is OK for Phase 2 testing (frontend recording)")
        # Don't raise - allow server to start for Phase 2 testing

    yield

    # Shutdown
    print("👋 Shutting down PrepWise Voice API")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="PrepWise Voice API",
    description="Voice and transcription service for interview preparation platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root endpoint - API information
    """
    return {
        "message": "PrepWise Voice API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "config": "/config",
            "transcribe": "/transcribe"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    Returns API status and configuration validation
    """
    try:
        # Check if API keys are configured
        config_summary = Config.get_config_summary()

        return {
            "status": "healthy",
            "service": "PrepWise Voice API",
            "version": "1.0.0",
            "api_keys_configured": config_summary["api_keys_configured"],
            "transcription_provider": config_summary.get("transcription_provider", "whisper"),
            "ready_for_requests": (
                config_summary["api_keys_configured"]["vapi"] if config_summary.get("transcription_provider") == "vapi"
                else config_summary["api_keys_configured"]["openai"]
            )
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )


@app.get("/config")
async def get_config():
    """
    Get non-sensitive configuration information
    """
    try:
        config_summary = Config.get_config_summary()
        return {
            "status": "success",
            "config": config_summary
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving configuration: {str(e)}"
        )


@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = Query(None, description="Language code (e.g., 'en', 'es', 'fr'). Default: auto-detect"),
    response_format: Optional[str] = Query("verbose_json", description="Response format: 'text', 'json', 'verbose_json', 'srt', 'vtt'"),
    include_timestamps: Optional[bool] = Query(True, description="Include word-level timestamps"),
    include_confidence: Optional[bool] = Query(True, description="Include confidence scores (requires verbose_json)"),
    chunk_large_files: Optional[bool] = Query(True, description="Automatically chunk files larger than 25MB")
):
    """
    Transcribe audio to text using OpenAI Whisper API with advanced features
    
    Features:
    - Automatic audio format conversion
    - Large file chunking (files > 25MB)
    - Word-level timestamps
    - Confidence scores
    - Retry logic for rate limits
    - Multiple response formats
    """
    try:
        # Check if API key is configured based on provider
        if Config.TRANSCRIPTION_PROVIDER == "vapi":
            if not Config.VAPI_API_KEY:
                raise HTTPException(
                    status_code=500,
                    detail="Vapi API key not configured. Please add VAPI_API_KEY to .env file."
                )
        else:
            if not Config.OPENAI_API_KEY:
                raise HTTPException(
                    status_code=500,
                    detail="OpenAI API key not configured. Please add OPENAI_API_KEY to .env file."
                )

        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        # Read file content
        contents = await file.read()
        file_size = len(contents)

        # Check file size
        if file_size == 0:
            raise HTTPException(status_code=400, detail="File is empty")

        # Get file extension
        file_ext = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
        
        # Validate format (more lenient - let Whisper handle format conversion)
        if file_ext and file_ext not in Config.SUPPORTED_FORMATS:
            # Warn but don't fail - Whisper may still accept it
            pass

        # Use transcription service (Vapi or Whisper based on config)
        if Config.TRANSCRIPTION_PROVIDER == "vapi":
            from utils.vapi_transcription_service import VapiTranscriptionService
            service = VapiTranscriptionService()
        else:
            from utils.transcription_service import TranscriptionService
            service = TranscriptionService()
        
        try:
            
            result = service.transcribe(
                audio_data=contents,
                filename=file.filename,
                language=language,
                response_format=response_format,
                include_timestamps=include_timestamps,
                include_confidence=include_confidence,
                chunk_large_files=chunk_large_files
            )

            # Add request metadata
            result["request_metadata"] = {
                "filename": file.filename,
                "file_size_bytes": file_size,
                "file_size_mb": round(file_size / 1024 / 1024, 2),
                "format": file_ext
            }

            return result

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            error_msg = str(e)
            if "Invalid API key" in error_msg or "authentication" in error_msg.lower():
                raise HTTPException(
                    status_code=401,
                    detail="Invalid OpenAI API key. Please check your API key in .env file."
                )
            elif "rate limit" in error_msg.lower():
                raise HTTPException(
                    status_code=429,
                    detail="OpenAI API rate limit exceeded. Please try again later."
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Transcription failed: {error_msg}"
                )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )


# This endpoint is a placeholder for future implementation
@app.post("/vapi/call/create")
async def create_vapi_call():
    """
    Create a Vapi call for real-time streaming
    Returns call ID and WebSocket URL for frontend connection
    """
    try:
        from config import Config
        
        if not Config.VAPI_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="Vapi API key not configured"
            )
        
        assistant_id = os.getenv("VAPI_ASSISTANT_ID")
        if not assistant_id:
            raise HTTPException(
                status_code=500,
                detail="VAPI_ASSISTANT_ID not configured"
            )
        
        # Create call via Vapi API
        import requests
        call_url = "https://api.vapi.ai/call"
        headers = {
            "Authorization": f"Bearer {Config.VAPI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # For web-based interviews, we need to use Vapi's WebSocket/streaming API
        # Vapi's REST API only supports phone calls, but web calls use WebSocket
        # Create a minimal call structure that can be used for web streaming
        
        # Try different approaches for web calls
        # Option 1: Check if Vapi has a web call endpoint
        # Option 2: Use WebSocket directly (frontend connects to Vapi)
        
        # For now, create a call that can be used for web streaming
        # The frontend will connect via WebSocket to stream audio
        call_data = {
            "assistantId": assistant_id,
        }
        
        # Try to get phone number (some Vapi setups might need it even for web)
        phone_numbers_url = "https://api.vapi.ai/phone-number"
        phone_response = requests.get(phone_numbers_url, headers=headers, timeout=10)
        
        phone_number_id = None
        if phone_response.status_code == 200:
            phone_numbers = phone_response.json()
            if isinstance(phone_numbers, list) and len(phone_numbers) > 0:
                phone_number_id = phone_numbers[0].get('id')
            elif isinstance(phone_numbers, dict) and phone_numbers.get('data') and len(phone_numbers.get('data', [])) > 0:
                phone_number_id = phone_numbers['data'][0].get('id')
        
        # If we have a phone number, add it (but we'll use it for web streaming, not actual phone call)
        if phone_number_id:
            call_data["phoneNumberId"] = phone_number_id
        
        # Note: Vapi's REST API might not support web calls directly
        # We may need to use their WebSocket API or SDK instead
        # For now, try creating without type (let Vapi decide) or use a workaround
        
        response = requests.post(call_url, json=call_data, headers=headers, timeout=30)
        
        if response.status_code not in [200, 201]:
            error_data = response.json() if response.content else {}
            error_msg = error_data.get('message', error_data.get('error', f"HTTP {response.status_code}"))
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to create Vapi call: {error_msg}"
            )
        
        call_info = response.json()
        
        return {
            "status": "success",
            "callId": call_info.get('id'),
            "serverUrl": call_info.get('serverUrl'),
            "status": call_info.get('status'),
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating Vapi call: {str(e)}"
        )


@app.get("/vapi/call/{call_id}/transcript")
async def get_vapi_call_transcript(call_id: str):
    """
    Get transcript from a Vapi call
    """
    try:
        from config import Config
        
        if not Config.VAPI_API_KEY:
            raise HTTPException(status_code=500, detail="Vapi API key not configured")
        
        import requests
        url = f"https://api.vapi.ai/call/{call_id}"
        headers = {
            "Authorization": f"Bearer {Config.VAPI_API_KEY}",
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to get call transcript"
            )
        
        call_data = response.json()
        
        # Extract transcript from call data
        messages = call_data.get('messages', [])
        transcript = call_data.get('transcript', '')
        
        # Get user messages (what the user said)
        user_messages = [msg.get('content', '') for msg in messages if msg.get('role') == 'user']
        full_transcript = ' '.join(user_messages) if user_messages else transcript
        
        return {
            "status": "success",
            "callId": call_id,
            "transcript": full_transcript,
            "messages": messages,
            "callStatus": call_data.get('status'),
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting transcript: {str(e)}"
        )


@app.post("/synthesize")
async def synthesize_speech(text: str):
    """
    Convert text to speech using OpenAI TTS
    (Placeholder - to be implemented in Phase 2)
    """
    return {
        "status": "not_implemented",
        "message": "Speech synthesis endpoint will be implemented in Phase 2",
        "received_text": text[:100] + "..." if len(text) > 100 else text
    }


if __name__ == "__main__":
    print("🚀 Starting PrepWise Voice API...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("❤️  Health Check: http://localhost:8000/health")
    print("")

    uvicorn.run(
        "main:app",  # Use string format for reload to work
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
