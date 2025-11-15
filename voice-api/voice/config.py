import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """
    Configuration class for PrepWise Voice API
    Loads settings from environment variables and provides defaults
    """

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    VAPI_API_KEY = os.getenv("VAPI_API_KEY")
    VAPI_PUBLIC_API_KEY = os.getenv("VAPI_PUBLIC_API_KEY")  # Public key for frontend web calls
    
    # Transcription Provider (whisper or vapi)
    TRANSCRIPTION_PROVIDER = os.getenv("TRANSCRIPTION_PROVIDER", "vapi").lower()  # Default to vapi

    # Audio Processing Settings
    MAX_AUDIO_SIZE_MB = int(os.getenv("MAX_AUDIO_SIZE_MB", "25"))
    MAX_AUDIO_SIZE_BYTES = MAX_AUDIO_SIZE_MB * 1024 * 1024

    SUPPORTED_FORMATS = ["webm", "mp3", "wav", "m4a", "ogg"]

    MAX_DURATION_SECONDS = int(os.getenv("MAX_DURATION_SECONDS", "600"))  # 10 minutes

    # Whisper API Settings
    WHISPER_MODEL = "whisper-1"
    WHISPER_RESPONSE_FORMAT = "text"  # Options: text, json, verbose_json, srt, vtt

    # TTS Settings
    TTS_MODEL = "tts-1"  # Options: tts-1, tts-1-hd
    TTS_VOICE = "nova"  # Options: alloy, echo, fable, onyx, nova, shimmer
    TTS_SPEED = 1.0  # Range: 0.25 to 4.0

    # File Storage
    UPLOAD_DIR = Path(__file__).parent / "uploads"
    OUTPUT_DIR = Path(__file__).parent / "outputs"

    @classmethod
    def validate(cls):
        """
        Validate required configuration settings
        Raises ValueError if required settings are missing
        """
        # Validate based on transcription provider
        if cls.TRANSCRIPTION_PROVIDER == "vapi":
            if not cls.VAPI_API_KEY:
                raise ValueError(
                    "VAPI_API_KEY not set in .env file. "
                    "Please add your Vapi API key to the .env file."
                )
        elif cls.TRANSCRIPTION_PROVIDER == "whisper":
            if not cls.OPENAI_API_KEY:
                raise ValueError(
                    "OPENAI_API_KEY not set in .env file. "
                    "Please add your OpenAI API key to the .env file."
                )

        # Create required directories if they don't exist
        cls.UPLOAD_DIR.mkdir(exist_ok=True)
        cls.OUTPUT_DIR.mkdir(exist_ok=True)

        return True

    @classmethod
    def get_config_summary(cls):
        """
        Returns a dictionary with non-sensitive configuration information
        """
        return {
            "max_audio_size_mb": cls.MAX_AUDIO_SIZE_MB,
            "max_duration_seconds": cls.MAX_DURATION_SECONDS,
            "supported_formats": cls.SUPPORTED_FORMATS,
            "whisper_model": cls.WHISPER_MODEL,
            "tts_model": cls.TTS_MODEL,
            "tts_voice": cls.TTS_VOICE,
            "api_keys_configured": {
                "openai": bool(cls.OPENAI_API_KEY),
                "elevenlabs": bool(cls.ELEVENLABS_API_KEY),
                "vapi": bool(cls.VAPI_API_KEY),
                "vapi_public": bool(cls.VAPI_PUBLIC_API_KEY)
            },
            "vapi_public_key": cls.VAPI_PUBLIC_API_KEY if cls.VAPI_PUBLIC_API_KEY else None,
            "transcription_provider": cls.TRANSCRIPTION_PROVIDER
        }


# Validate configuration on import (will raise error if invalid)
# Comment this out during development if you don't have API keys yet
# Config.validate()
